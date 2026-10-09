from pathlib import Path
import subprocess
import re
import csv
import math
import hashlib

from pvt_config import (
    PROCESS_CORNERS,
    TEMPERATURES_C,
    SUPPLIES_V,
    CL_PF,
    A0_MIN_DB,
    PM_MIN_DEG,
    GM_MIN_DB,
)


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

WORK = ROOT / "work"

AC_NETLIST = WORK / "tb_ota_2stage_ac.spice"
PSRR_NETLIST = WORK / "tb_ota_2stage_psrr.spice"

OUT = WORK / "pvt"
LOGS = OUT / "logs"

GEN = ROOT / "report" / "generated"

OUT.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
GEN.mkdir(parents=True, exist_ok=True)


# ============================================================
# Generic helpers
# ============================================================

def remove_control(text):
    return re.sub(
        r"(?ms)^\s*\.control\b.*?^\s*\.endc\s*\n?",
        "",
        text,
    )


def insert_before_end(text, block):

    matches = list(
        re.finditer(
            r"(?mi)^\s*\.end\s*$",
            text,
        )
    )

    if not matches:
        return text + "\n" + block + "\n.end\n"

    pos = matches[-1].start()

    return (
        text[:pos]
        + block
        + "\n"
        + text[pos:]
    )


def set_corner(text, corner):

    pattern = (
        r"(?mi)^"
        r"(\.lib\s+\S*sky130\.lib\.spice\s+)"
        r"\S+"
    )

    text, count = re.subn(
        pattern,
        rf"\g<1>{corner}",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError(
            f"Could not replace process corner with {corner}"
        )

    return text


def set_temperature(text, temp_c):

    pattern = r"(?mi)^\s*\.temp\s+.*$"

    if re.search(pattern, text):

        return re.sub(
            pattern,
            f".temp {temp_c}",
            text,
            count=1,
        )

    return insert_before_end(
        text,
        f".temp {temp_c}",
    )


def set_vdd(text, vdd, psrr=False):

    pattern = (
        r"(?mi)^"
        r"V1\s+VDD\s+0\s+.*$"
    )

    if psrr:

        replacement = (
            f"V1 VDD 0 DC {vdd:g} AC 1"
        )

    else:

        replacement = (
            f"V1 VDD 0 {vdd:g}"
        )

    text, count = re.subn(
        pattern,
        replacement,
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError(
            "Could not replace VDD source V1."
        )

    return text


def set_cl(text, cl_pf):

    pattern = (
        r"(?mi)^"
        r"(CL\s+Vout\s+0\s+)"
        r"\S+"
    )

    value = f"{cl_pf:g}p"

    text, count = re.subn(
        pattern,
        rf"\g<1>{value}",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError(
            "Could not replace CL."
        )

    return text


def insert_control(text, control):
    return insert_before_end(
        text,
        control,
    )


def number_tag(value):
    return f"{value:g}".replace(".", "p")


def temp_tag(temp):

    if temp < 0:
        return f"M{abs(temp)}C"

    return f"P{temp}C"


def condition_string(row):

    return (
        f"{row['corner']} / "
        f"{row['temp_C']:+g}C / "
        f"{row['VDD_V']:.2f}V"
    )


# ============================================================
# File-data helpers
# ============================================================

def read_three_column_data(path):

    rows = []

    with open(path) as f:

        for line in f:

            if line.lstrip().startswith("frequency"):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            try:
                rows.append(
                    (
                        float(parts[0]),
                        float(parts[1]),
                        float(parts[2]),
                    )
                )

            except ValueError:
                pass

    if not rows:
        raise RuntimeError(
            f"No AC data found in {path}"
        )

    return rows


def read_two_column_data(path):

    rows = []

    with open(path) as f:

        for line in f:

            if line.lstrip().startswith("frequency"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            try:
                rows.append(
                    (
                        float(parts[0]),
                        float(parts[1]),
                    )
                )

            except ValueError:
                pass

    if not rows:
        raise RuntimeError(
            f"No data found in {path}"
        )

    return rows


def interpolate_log_x(
    x1,
    y1,
    x2,
    y2,
    target_y,
):

    lx1 = math.log10(x1)
    lx2 = math.log10(x2)

    frac = (
        (target_y - y1)
        / (y2 - y1)
    )

    lx = (
        lx1
        + frac * (lx2 - lx1)
    )

    return 10 ** lx, frac


# ============================================================
# AC metrics
# ============================================================

def extract_ac_metrics(path):

    rows = read_three_column_data(path)

    freq = [r[0] for r in rows]
    gain = [r[1] for r in rows]
    phase = [r[2] for r in rows]

    # Low-frequency gain at first point (~1 Hz)
    a0 = gain[0]

    # --------------------------------------------------------
    # Unity-gain frequency and phase margin
    # --------------------------------------------------------

    ugf_index = None

    for i in range(len(gain) - 1):

        if (
            gain[i] >= 0
            and gain[i + 1] < 0
        ):
            ugf_index = i
            break

    if ugf_index is None:

        raise RuntimeError(
            f"No 0-dB crossing found in {path}"
        )

    i = ugf_index

    ugf, frac = interpolate_log_x(
        freq[i],
        gain[i],
        freq[i + 1],
        gain[i + 1],
        0.0,
    )

    phase_ugf = (
        phase[i]
        + frac
        * (
            phase[i + 1]
            - phase[i]
        )
    )

    pm = 180.0 + phase_ugf

    # --------------------------------------------------------
    # Gain margin
    #
    # Find first -180 deg phase crossing.
    # GM = -gain at that crossing.
    # --------------------------------------------------------

    phase_index = None

    for i in range(len(phase) - 1):

        if (
            phase[i] > -180.0
            and phase[i + 1] <= -180.0
        ):
            phase_index = i
            break

    if phase_index is None:

        gm_db = math.inf

    else:

        i = phase_index

        f180, frac = interpolate_log_x(
            freq[i],
            phase[i],
            freq[i + 1],
            phase[i + 1],
            -180.0,
        )

        gain_at_180 = (
            gain[i]
            + frac
            * (
                gain[i + 1]
                - gain[i]
            )
        )

        gm_db = -gain_at_180

    return {
        "A0_dB": a0,
        "UGF_Hz": ugf,
        "PM_deg": pm,
        "GM_dB": gm_db,
    }


# ============================================================
# PSRR extraction
# ============================================================

def extract_at_frequency(path, target_freq):

    rows = read_two_column_data(path)

    for i in range(len(rows) - 1):

        f1, y1 = rows[i]
        f2, y2 = rows[i + 1]

        if f1 <= target_freq <= f2:

            if f1 == target_freq:
                return y1

            if f2 == target_freq:
                return y2

            lx1 = math.log10(f1)
            lx2 = math.log10(f2)
            lxt = math.log10(target_freq)

            frac = (
                (lxt - lx1)
                / (lx2 - lx1)
            )

            return (
                y1
                + frac
                * (y2 - y1)
            )

    raise RuntimeError(
        f"{target_freq} Hz not found in {path}"
    )


# ============================================================
# IQ parser
# ============================================================

def extract_scalar(text, name):

    pattern = (
        rf"(?mi)^\s*{re.escape(name)}\s*=\s*"
        rf"([+-]?"
        rf"(?:\d+(?:\.\d*)?|\.\d+)"
        rf"(?:[eE][+-]?\d+)?)"
    )

    matches = re.findall(
        pattern,
        text,
    )

    if not matches:
        raise RuntimeError(
            f"Could not find {name} in ngspice output."
        )

    return float(matches[-1])


# ============================================================
# Load source netlists
# ============================================================

if not AC_NETLIST.exists():
    raise SystemExit(
        "Missing work/tb_ota_2stage_ac.spice\n"
        "Regenerate the Xschem AC netlist first."
    )


if not PSRR_NETLIST.exists():
    raise SystemExit(
        "Missing work/tb_ota_2stage_psrr.spice\n"
        "Regenerate the Xschem PSRR netlist first."
    )


base_ac = AC_NETLIST.read_text()
base_psrr = PSRR_NETLIST.read_text()


# ============================================================
# Clear old generated PVT data
# ============================================================

for path in OUT.glob("*.dat"):
    path.unlink()

for path in OUT.glob("_tmp_*.spice"):
    path.unlink()


# ============================================================
# Sweep
# ============================================================

results = []

total_cases = (
    len(PROCESS_CORNERS)
    * len(TEMPERATURES_C)
    * len(SUPPLIES_V)
)

case_number = 0


for corner_name, pdk_corner in PROCESS_CORNERS:

    for temp_c in TEMPERATURES_C:

        for vdd in SUPPLIES_V:

            case_number += 1

            tag = (
                f"{corner_name}_"
                f"{temp_tag(temp_c)}_"
                f"{number_tag(vdd)}V"
            )

            print(
                f"[{case_number:02d}/{total_cases}] "
                f"{corner_name:4s}  "
                f"{temp_c:+4d} C  "
                f"{vdd:.2f} V ... ",
                end="",
                flush=True,
            )

            # =================================================
            # AC / IQ
            # =================================================

            ac_dat = OUT / f"ac_{tag}.dat"
            ac_tmp = OUT / "_tmp_ac.spice"

            text = remove_control(base_ac)

            text = set_corner(
                text,
                pdk_corner,
            )

            text = set_temperature(
                text,
                temp_c,
            )

            text = set_vdd(
                text,
                vdd,
                psrr=False,
            )

            text = set_cl(
                text,
                CL_PF,
            )

            ac_control = f"""
.control

set wr_singlescale
set wr_vecnames

op

let pvt_iq = -i(V1)
let pvt_vout = v(Vout)

print pvt_iq
print pvt_vout

ac dec 200 1 100Meg

let vid = v(Vin_P)-v(Vin_N)
let aol = v(Vout)/vid

let gain_db = db(aol)
let phase_deg = 180/PI*cph(aol)

wrdata {ac_dat} gain_db phase_deg

quit

.endc
"""

            text = insert_control(
                text,
                ac_control,
            )

            ac_tmp.write_text(text)

            ac_proc = subprocess.run(
                [
                    "ngspice",
                    "-b",
                    str(ac_tmp),
                ],
                cwd=WORK,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            (
                LOGS / f"ac_{tag}.log"
            ).write_text(
                ac_proc.stdout
            )

            if (
                ac_proc.returncode != 0
                or not ac_dat.exists()
            ):

                print("FAILED")

                raise RuntimeError(
                    f"AC simulation failed for {tag}\n"
                    f"See {LOGS / f'ac_{tag}.log'}"
                )

            ac_metrics = extract_ac_metrics(
                ac_dat
            )

            iq = extract_scalar(
                ac_proc.stdout,
                "pvt_iq",
            )

            vout_dc = extract_scalar(
                ac_proc.stdout,
                "pvt_vout",
            )

            # =================================================
            # PSRR+
            # =================================================

            psrr_dat = OUT / f"psrr_{tag}.dat"
            psrr_tmp = OUT / "_tmp_psrr.spice"

            text = remove_control(
                base_psrr
            )

            text = set_corner(
                text,
                pdk_corner,
            )

            text = set_temperature(
                text,
                temp_c,
            )

            text = set_vdd(
                text,
                vdd,
                psrr=True,
            )

            text = set_cl(
                text,
                CL_PF,
            )

            psrr_control = f"""
.control

set wr_singlescale
set wr_vecnames

ac dec 200 1 100Meg

let avdd = v(Vout)/v(VDD)
let psrr_plus = -db(avdd)

wrdata {psrr_dat} psrr_plus

quit

.endc
"""

            text = insert_control(
                text,
                psrr_control,
            )

            psrr_tmp.write_text(
                text
            )

            psrr_proc = subprocess.run(
                [
                    "ngspice",
                    "-b",
                    str(psrr_tmp),
                ],
                cwd=WORK,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            (
                LOGS / f"psrr_{tag}.log"
            ).write_text(
                psrr_proc.stdout
            )

            if (
                psrr_proc.returncode != 0
                or not psrr_dat.exists()
            ):

                print("FAILED")

                raise RuntimeError(
                    f"PSRR simulation failed for {tag}\n"
                    f"See {LOGS / f'psrr_{tag}.log'}"
                )

            psrr_1k = extract_at_frequency(
                psrr_dat,
                1e3,
            )

            row = {
                "corner": corner_name,
                "pdk_corner": pdk_corner,
                "temp_C": temp_c,
                "VDD_V": vdd,

                "A0_dB":
                    ac_metrics["A0_dB"],

                "UGF_Hz":
                    ac_metrics["UGF_Hz"],

                "PM_deg":
                    ac_metrics["PM_deg"],

                "GM_dB":
                    ac_metrics["GM_dB"],

                "IQ_A": iq,

                "PSRR_1kHz_dB":
                    psrr_1k,

                "Vout_DC_V":
                    vout_dc,
            }

            results.append(row)

            print("OK")


# ============================================================
# CSV
# ============================================================

csv_path = (
    OUT
    / "pvt_results.csv"
)

with open(
    csv_path,
    "w",
    newline="",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=results[0].keys(),
    )

    writer.writeheader()
    writer.writerows(results)


# ============================================================
# Nominal / worst-case helpers
# ============================================================

def nominal_row():

    for row in results:

        if (
            row["corner"] == "TT"
            and row["temp_C"] == 27
            and abs(
                row["VDD_V"] - 1.80
            ) < 1e-9
        ):

            return row

    raise RuntimeError(
        "Nominal TT / 27C / 1.80V case not found."
    )


nominal = nominal_row()


def minimum(metric):
    return min(
        results,
        key=lambda r: r[metric],
    )


def maximum(metric):
    return max(
        results,
        key=lambda r: r[metric],
    )


worst_a0 = minimum("A0_dB")
worst_ugf = minimum("UGF_Hz")
max_ugf = maximum("UGF_Hz")

worst_pm = minimum("PM_deg")

finite_gm_rows = [
    r
    for r in results
    if math.isfinite(r["GM_dB"])
]

if finite_gm_rows:

    worst_gm = min(
        finite_gm_rows,
        key=lambda r: r["GM_dB"],
    )

else:

    worst_gm = None

min_iq = minimum("IQ_A")
max_iq = maximum("IQ_A")

worst_psrr = minimum(
    "PSRR_1kHz_dB"
)


# ============================================================
# Pass / fail
# ============================================================

pass_a0 = (
    worst_a0["A0_dB"]
    >= A0_MIN_DB
)

pass_pm = (
    worst_pm["PM_deg"]
    >= PM_MIN_DEG
)

if worst_gm is None:

    pass_gm = True

else:

    pass_gm = (
        worst_gm["GM_dB"]
        > GM_MIN_DB
    )


# ============================================================
# Formatting
# ============================================================

def status(flag):
    return "PASS" if flag else "FAIL"


def gm_string(value):

    if math.isinf(value):
        return "> simulation range"

    return f"{value:.1f} dB"


# ============================================================
# Text summary
# ============================================================

summary_lines = []

summary_lines.append(
    "PVT SUMMARY"
)

summary_lines.append(
    "==========="
)

summary_lines.append("")

summary_lines.append(
    f"Cases: {len(results)}"
)

summary_lines.append(
    f"Load: {CL_PF:g} pF"
)

summary_lines.append("")

summary_lines.append(
    "Nominal:"
)

summary_lines.append(
    "  TT / +27C / 1.80V"
)

summary_lines.append(
    f"  A0       = "
    f"{nominal['A0_dB']:.2f} dB"
)

summary_lines.append(
    f"  UGF      = "
    f"{nominal['UGF_Hz']/1e3:.1f} kHz"
)

summary_lines.append(
    f"  PM       = "
    f"{nominal['PM_deg']:.2f} deg"
)

summary_lines.append(
    f"  GM       = "
    f"{gm_string(nominal['GM_dB'])}"
)

summary_lines.append(
    f"  IQ       = "
    f"{nominal['IQ_A']*1e6:.3f} uA"
)

summary_lines.append(
    f"  PSRR 1k  = "
    f"{nominal['PSRR_1kHz_dB']:.2f} dB"
)

summary_lines.append("")

summary_lines.append(
    "Worst / range:"
)

summary_lines.append(
    f"  A0 min   = "
    f"{worst_a0['A0_dB']:.2f} dB  "
    f"[{condition_string(worst_a0)}]"
)

summary_lines.append(
    f"  UGF min  = "
    f"{worst_ugf['UGF_Hz']/1e3:.1f} kHz  "
    f"[{condition_string(worst_ugf)}]"
)

summary_lines.append(
    f"  UGF max  = "
    f"{max_ugf['UGF_Hz']/1e3:.1f} kHz  "
    f"[{condition_string(max_ugf)}]"
)

summary_lines.append(
    f"  PM min   = "
    f"{worst_pm['PM_deg']:.2f} deg  "
    f"[{condition_string(worst_pm)}]"
)

if worst_gm is not None:

    summary_lines.append(
        f"  GM min   = "
        f"{worst_gm['GM_dB']:.2f} dB  "
        f"[{condition_string(worst_gm)}]"
    )

else:

    summary_lines.append(
        "  GM       = no -180 deg crossing "
        "within simulation range"
    )

summary_lines.append(
    f"  IQ min   = "
    f"{min_iq['IQ_A']*1e6:.3f} uA  "
    f"[{condition_string(min_iq)}]"
)

summary_lines.append(
    f"  IQ max   = "
    f"{max_iq['IQ_A']*1e6:.3f} uA  "
    f"[{condition_string(max_iq)}]"
)

summary_lines.append(
    f"  PSRR min = "
    f"{worst_psrr['PSRR_1kHz_dB']:.2f} dB  "
    f"[{condition_string(worst_psrr)}]"
)

summary_lines.append("")

summary_lines.append(
    "Hard requirements:"
)

summary_lines.append(
    f"  A0 >= {A0_MIN_DB:g} dB : "
    f"{status(pass_a0)}"
)

summary_lines.append(
    f"  PM >= {PM_MIN_DEG:g} deg : "
    f"{status(pass_pm)}"
)

summary_lines.append(
    f"  GM >  {GM_MIN_DB:g} dB : "
    f"{status(pass_gm)}"
)


summary_path = (
    OUT
    / "pvt_summary.txt"
)

summary_path.write_text(
    "\n".join(summary_lines)
    + "\n"
)


# ============================================================
# Reproducibility manifest
# ============================================================

manifest = (
    OUT
    / "pvt_manifest.txt"
)

ac_hash = hashlib.sha256(
    base_ac.encode()
).hexdigest()

psrr_hash = hashlib.sha256(
    base_psrr.encode()
).hexdigest()

manifest.write_text(
f"""PVT REGRESSION MANIFEST
=======================

AC source netlist:
{AC_NETLIST}

AC SHA256:
{ac_hash}

PSRR source netlist:
{PSRR_NETLIST}

PSRR SHA256:
{psrr_hash}

Process corners:
{PROCESS_CORNERS}

Temperatures:
{TEMPERATURES_C}

Supplies:
{SUPPLIES_V}

Load:
{CL_PF} pF

Hard requirements:
A0 >= {A0_MIN_DB} dB
PM >= {PM_MIN_DEG} deg
GM > {GM_MIN_DB} dB
"""
)


# ============================================================
# Generated LaTeX summary table
# ============================================================

def latex_condition(row):

    return (
        f"{row['corner']} / "
        f"${row['temp_C']:+g}^\\circ\\mathrm{{C}}$ / "
        f"{row['VDD_V']:.2f} V"
    )


if worst_gm is None:

    gm_worst_value = (
        r"$>$ simulation range"
    )

    gm_worst_condition = "--"

else:

    gm_worst_value = (
        f"{worst_gm['GM_dB']:.1f} dB"
    )

    gm_worst_condition = (
        latex_condition(worst_gm)
    )


latex_table = (
    GEN
    / "pvt_summary_table.tex"
)

latex_table.write_text(
f"""% AUTO-GENERATED -- DO NOT EDIT

\\begin{{table}}[ht]
    \\centering
    \\caption{{Main electrical performance over the
    45-point PVT matrix at $C_L={CL_PF:g}~\\mathrm{{pF}}$.}}
    \\label{{tab:pvt_summary}}

    \\begin{{tabular}}{{lccc}}
        \\hline
        Metric & Nominal & Worst PVT & Worst condition \\\\
        \\hline

        DC gain &
        {nominal['A0_dB']:.1f} dB &
        {worst_a0['A0_dB']:.1f} dB &
        {latex_condition(worst_a0)} \\\\

        UGF &
        {nominal['UGF_Hz']/1e3:.0f} kHz &
        {worst_ugf['UGF_Hz']/1e3:.0f} kHz &
        {latex_condition(worst_ugf)} \\\\

        Phase margin &
        {nominal['PM_deg']:.1f}$^\\circ$ &
        {worst_pm['PM_deg']:.1f}$^\\circ$ &
        {latex_condition(worst_pm)} \\\\

        Gain margin &
        {gm_string(nominal['GM_dB'])} &
        {gm_worst_value} &
        {gm_worst_condition} \\\\

        Supply current &
        {nominal['IQ_A']*1e6:.2f} $\\mu$A &
        {max_iq['IQ_A']*1e6:.2f} $\\mu$A &
        {latex_condition(max_iq)} \\\\

        PSRR$^+$ @ 1 kHz &
        {nominal['PSRR_1kHz_dB']:.1f} dB &
        {worst_psrr['PSRR_1kHz_dB']:.1f} dB &
        {latex_condition(worst_psrr)} \\\\

        \\hline
    \\end{{tabular}}
\\end{{table}}
"""
)


# ============================================================
# Cleanup
# ============================================================

for path in [
    OUT / "_tmp_ac.spice",
    OUT / "_tmp_psrr.spice",
]:

    path.unlink(
        missing_ok=True
    )


# ============================================================
# Console output
# ============================================================

print()
print(
    "\n".join(summary_lines)
)

print()
print("Generated:")
print(f"  {csv_path}")
print(f"  {summary_path}")
print(f"  {manifest}")
print(f"  {latex_table}")
