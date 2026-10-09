from pathlib import Path
import subprocess
import hashlib
import re
import csv
import math


# ============================================================
# Project paths
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

WORK = ROOT / "work"
NETLIST = WORK / "tb_ota_2stage_ac.spice"

OUT = WORK / "transistor"
GEN = ROOT / "report" / "generated"

OUT.mkdir(parents=True, exist_ok=True)
GEN.mkdir(parents=True, exist_ok=True)


# ============================================================
# Regression definition
# ============================================================

CL_CASES = [
    (2.0, "2p"),
    (4.0, "4p"),
]

# Nominal compensation-resistor cases.
#
# None  -> resistor replaced by ~ideal short reference
# 19k   -> physical SKY130 xhigh poly
# 110k  -> physical SKY130 xhigh poly
# 180k  -> physical SKY130 xhigh poly
#
RZ_CASES = [
    (None, "SHORT"),
    (19e3, "19k"),
    (110e3, "110k"),
    (180e3, "180k"),
]

R_XHIGH_SHEET = 2000.0
R_XHIGH_WIDTH_UM = 0.35

CAP_MODEL = "sky130_fd_pr__cap_mim_m3_1"
RES_MODEL = "sky130_fd_pr__res_xhigh_po_0p35"


# ============================================================
# Generic helpers
# ============================================================

def number_tag(value):
    return f"{value:g}".replace(".", "p")


def remove_control(text):
    return re.sub(
        r"(?ms)^\s*\.control\b.*?^\s*\.endc\s*\n?",
        "",
        text,
    )


def insert_control(text, control):

    matches = list(
        re.finditer(
            r"(?mi)^\s*\.end\s*$",
            text,
        )
    )

    if matches:
        pos = matches[-1].start()
        return (
            text[:pos]
            + control
            + "\n"
            + text[pos:]
        )

    return (
        text
        + "\n"
        + control
        + "\n.end\n"
    )


# ============================================================
# SPICE logical-line helpers
# ============================================================

def logical_blocks(text):

    lines = text.splitlines(keepends=True)

    blocks = []

    i = 0

    while i < len(lines):

        block = [lines[i]]

        j = i + 1

        while (
            j < len(lines)
            and lines[j].lstrip().startswith("+")
        ):
            block.append(lines[j])
            j += 1

        blocks.append("".join(block))

        i = j

    return blocks


def flatten_block(block):

    return re.sub(
        r"\n\s*\+\s*",
        " ",
        block,
    ).strip()


def find_model_block(text, model):

    matches = []

    for block in logical_blocks(text):

        flat = flatten_block(block)

        if model.lower() in flat.lower():
            matches.append(block)

    if len(matches) != 1:

        raise RuntimeError(
            f"Expected exactly one instance of {model}, "
            f"found {len(matches)}."
        )

    return matches[0]


def read_param(block, param):

    flat = flatten_block(block)

    match = re.search(
        rf"\b{re.escape(param)}\s*=\s*"
        rf"([+-]?[0-9.eE]+)",
        flat,
        re.I,
    )

    if not match:

        raise RuntimeError(
            f"Parameter {param} not found in:\n{flat}"
        )

    return float(match.group(1))


def replace_param_in_model(
    text,
    model,
    param,
    value,
):

    block = find_model_block(text, model)

    pattern = (
        rf"(\b{re.escape(param)}\s*=\s*)"
        rf"([^\s]+)"
    )

    new_block, count = re.subn(
        pattern,
        rf"\g<1>{value}",
        block,
        count=1,
        flags=re.I,
    )

    if count != 1:

        raise RuntimeError(
            f"Could not replace {param} "
            f"for {model}."
        )

    return text.replace(
        block,
        new_block,
        1,
    )


# ============================================================
# Physical compensation-device helpers
# ============================================================

def capacitor_nominal_ff(
    W_um,
    L_um,
    MF,
):
    """
    Nominal value displayed by the installed
    SKY130 Xschem cap_mim_m3_1 symbol:

        C = MF * [
            W*L*2 fF/um^2
            + (W+L)*0.38 fF/um
        ]
    """

    return MF * (
        W_um * L_um * 2.0
        + (W_um + L_um) * 0.38
    )


def resistor_length_um(
    resistance_ohm,
    mult,
):
    """
    Xschem nominal xhigh-poly relation:

        R = 2000 * L / 0.35 / mult
    """

    return (
        resistance_ohm
        * R_XHIGH_WIDTH_UM
        * mult
        / R_XHIGH_SHEET
    )


def resistor_nominal_ohm(
    L_um,
    mult,
):

    return (
        R_XHIGH_SHEET
        * L_um
        / R_XHIGH_WIDTH_UM
        / mult
    )


def replace_resistor_with_short(text):

    block = find_model_block(
        text,
        RES_MODEL,
    )

    flat = flatten_block(block)

    tokens = flat.split()

    if not tokens:
        raise RuntimeError(
            "Empty RMILLER block."
        )

    try:
        model_idx = next(
            i
            for i, tok in enumerate(tokens)
            if RES_MODEL.lower()
            in tok.lower()
        )

    except StopIteration:

        raise RuntimeError(
            "Could not locate resistor model token."
        )

    pins = tokens[1:model_idx]

    if len(pins) < 2:

        raise RuntimeError(
            "Could not determine RMILLER P/M pins."
        )

    p_node = pins[0]
    m_node = pins[1]

    short_line = (
        f"R__RZ_SHORT "
        f"{p_node} "
        f"{m_node} "
        f"1m\n"
    )

    return text.replace(
        block,
        short_line,
        1,
    )


# ============================================================
# Load-capacitance helper
# ============================================================

def replace_load_cap(
    text,
    value,
):

    pattern = (
        r"(?mi)^"
        r"(CL\s+\S+\s+\S+\s+)"
        r"\S+"
    )

    new_text, count = re.subn(
        pattern,
        rf"\g<1>{value}",
        text,
        count=1,
    )

    if count != 1:

        raise RuntimeError(
            "Could not uniquely replace CL."
        )

    return new_text


# ============================================================
# AC result extraction
# ============================================================

def load_wrdata(path):

    rows = []

    with open(path) as f:

        for line in f:

            if line.lstrip().startswith(
                "frequency"
            ):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            try:
                rows.append(
                    tuple(
                        map(
                            float,
                            parts[:3],
                        )
                    )
                )

            except ValueError:
                pass

    if not rows:

        raise RuntimeError(
            f"No numerical data found in {path}"
        )

    return rows


def extract_metrics(path):

    rows = load_wrdata(path)

    freq = [r[0] for r in rows]
    gain = [r[1] for r in rows]
    phase = [r[2] for r in rows]

    a0 = gain[0]

    crossing = None

    for i in range(
        len(gain) - 1
    ):

        if (
            gain[i] >= 0
            and gain[i + 1] < 0
        ):
            crossing = i
            break

    if crossing is None:

        raise RuntimeError(
            f"No 0-dB crossing in {path}"
        )

    i = crossing

    x1 = math.log10(freq[i])
    x2 = math.log10(freq[i + 1])

    frac = (
        (0.0 - gain[i])
        / (
            gain[i + 1]
            - gain[i]
        )
    )

    xu = (
        x1
        + frac
        * (x2 - x1)
    )

    ugf = 10 ** xu

    phase_ugf = (
        phase[i]
        + frac
        * (
            phase[i + 1]
            - phase[i]
        )
    )

    pm = 180.0 + phase_ugf

    return (
        a0,
        ugf,
        phase_ugf,
        pm,
    )


# ============================================================
# Load source netlist
# ============================================================

if not NETLIST.exists():

    raise SystemExit(
        "\nERROR: AC netlist not found.\n\n"
        "Regenerate tb_ota_2stage_ac.sch "
        "from Xschem first.\n"
    )


base = NETLIST.read_text()


# ============================================================
# Read physical CMILLER
# ============================================================

cap_block = find_model_block(
    base,
    CAP_MODEL,
)

cap_W = read_param(
    cap_block,
    "W",
)

cap_L = read_param(
    cap_block,
    "L",
)

cap_MF = read_param(
    cap_block,
    "MF",
)

cap_nom_ff = capacitor_nominal_ff(
    cap_W,
    cap_L,
    cap_MF,
)

cap_tag = (
    f"{number_tag(cap_nom_ff)}fF"
)


# ============================================================
# Read physical RMILLER
# ============================================================

res_block = find_model_block(
    base,
    RES_MODEL,
)

res_mult = read_param(
    res_block,
    "mult",
)

res_base_L = read_param(
    res_block,
    "L",
)

res_base_nom = resistor_nominal_ohm(
    res_base_L,
    res_mult,
)


# ============================================================
# Remove previous automatically generated data
# ============================================================

for path in OUT.glob(
    "ac_CL*_CM*_RZ*.dat"
):
    path.unlink()

for path in OUT.glob(
    "ac_CL*_CM*_RZ*.log"
):
    path.unlink()


# ============================================================
# Run AC regression
# ============================================================

results = []

for cl_pf, cl_spice in CL_CASES:

    for rz_target, rz_label in RZ_CASES:

        text = remove_control(base)

        text = replace_load_cap(
            text,
            cl_spice,
        )

        if rz_target is None:

            text = (
                replace_resistor_with_short(
                    text
                )
            )

            rz_nom = 0.0
            rz_length = None
            rz_tag = "SHORT"

        else:

            rz_length = resistor_length_um(
                rz_target,
                res_mult,
            )

            text = replace_param_in_model(
                text,
                RES_MODEL,
                "L",
                f"{rz_length:.8g}",
            )

            rz_nom = resistor_nominal_ohm(
                rz_length,
                res_mult,
            )

            rz_tag = (
                f"{number_tag(rz_nom / 1e3)}k"
            )

        filename = (
            f"ac_"
            f"CL{number_tag(cl_pf)}pF_"
            f"CM{cap_tag}_"
            f"RZ{rz_tag}.dat"
        )

        logfile = (
            filename.replace(
                ".dat",
                ".log",
            )
        )

        dat_path = OUT / filename

        control = f"""
.control

set wr_singlescale
set wr_vecnames

ac dec 200 1 100Meg

let vid = v(Vin_P)-v(Vin_N)
let aol = v(Vout)/vid

let gain_db = db(aol)
let phase_deg = 180/PI*cph(aol)

wrdata {dat_path} gain_db phase_deg

quit

.endc
"""

        text = insert_control(
            text,
            control,
        )

        temp_netlist = (
            OUT
            / "_tmp_ac_case.spice"
        )

        temp_netlist.write_text(
            text
        )

        proc = subprocess.run(
            [
                "ngspice",
                "-b",
                str(temp_netlist),
            ],
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        log_path = (
            OUT
            / logfile
        )

        log_path.write_text(
            proc.stdout
        )

        if not dat_path.exists():

            print(proc.stdout)

            raise RuntimeError(
                f"Simulation failed:\n"
                f"{filename}"
            )

        (
            a0,
            ugf,
            phase_ugf,
            pm,
        ) = extract_metrics(
            dat_path
        )

        results.append(
            {
                "filename": filename,
                "CL_pF": cl_pf,

                "CM_model": CAP_MODEL,
                "CM_W_um": cap_W,
                "CM_L_um": cap_L,
                "CM_MF": cap_MF,
                "CM_nom_fF": cap_nom_ff,

                "RZ_mode": rz_label,
                "RZ_model": (
                    "SHORT"
                    if rz_target is None
                    else RES_MODEL
                ),

                "RZ_L_um": (
                    ""
                    if rz_length is None
                    else rz_length
                ),

                "RZ_mult": (
                    ""
                    if rz_target is None
                    else res_mult
                ),

                "RZ_nom_ohm": rz_nom,

                "A0_dB": a0,
                "UGF_Hz": ugf,
                "phase_UGF_deg": phase_ugf,
                "PM_deg": pm,
            }
        )

        print(
            f"{filename:<55}"
            f"A0={a0:6.2f} dB  "
            f"UGF={ugf/1e3:8.1f} kHz  "
            f"PM={pm:6.2f} deg"
        )


# ============================================================
# Summary CSV
# ============================================================

summary = (
    OUT
    / "ac_summary.csv"
)

with open(
    summary,
    "w",
    newline="",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=results[0].keys(),
    )

    writer.writeheader()

    writer.writerows(
        results
    )


# ============================================================
# Netlist / physical-device manifest
# ============================================================

digest = hashlib.sha256(
    base.encode()
).hexdigest()

manifest = (
    OUT
    / "ac_manifest.txt"
)

with open(
    manifest,
    "w",
) as f:

    f.write(
        "TRANSISTOR-LEVEL AC REGRESSION\n"
    )

    f.write(
        "==============================\n\n"
    )

    f.write(
        f"Source netlist:\n"
        f"  {NETLIST}\n\n"
    )

    f.write(
        f"Netlist SHA256:\n"
        f"  {digest}\n\n"
    )

    f.write(
        "Physical CMILLER\n"
    )

    f.write(
        "----------------\n"
    )

    f.write(
        f"Model : {CAP_MODEL}\n"
    )

    f.write(
        f"W     : {cap_W} um\n"
    )

    f.write(
        f"L     : {cap_L} um\n"
    )

    f.write(
        f"MF    : {cap_MF:g}\n"
    )

    f.write(
        f"Cnom  : {cap_nom_ff:.3f} fF\n\n"
    )

    f.write(
        "Physical RMILLER base design\n"
    )

    f.write(
        "----------------------------\n"
    )

    f.write(
        f"Model : {RES_MODEL}\n"
    )

    f.write(
        f"L     : {res_base_L} um\n"
    )

    f.write(
        f"mult  : {res_mult:g}\n"
    )

    f.write(
        f"Rnom  : "
        f"{res_base_nom/1e3:.3f} kohm\n\n"
    )

    f.write(
        "Regression RZ cases\n"
    )

    f.write(
        "-------------------\n"
    )

    for r in results:

        if r["CL_pF"] != 4.0:
            continue

        if r["RZ_mode"] == "SHORT":

            f.write(
                "SHORT : "
                "1 milliohm ideal reference\n"
            )

        else:

            f.write(
                f"{r['RZ_mode']} : "
                f"L={float(r['RZ_L_um']):.4f} um, "
                f"Rnom={float(r['RZ_nom_ohm'])/1e3:.3f} kohm\n"
            )


# ============================================================
# Helpers for generated report data
# ============================================================

def get_result(
    cl,
    rz_mode,
):

    for result in results:

        if (
            result["CL_pF"] == cl
            and result["RZ_mode"]
            == rz_mode
        ):
            return result

    raise RuntimeError(
        f"Missing result "
        f"CL={cl}, "
        f"RZ={rz_mode}"
    )


r2_110 = get_result(
    2.0,
    "110k",
)

r4_short = get_result(
    4.0,
    "SHORT",
)

r4_19 = get_result(
    4.0,
    "19k",
)

r4_110 = get_result(
    4.0,
    "110k",
)

r2_180 = get_result(
    2.0,
    "180k",
)

r4_180 = get_result(
    4.0,
    "180k",
)

# ============================================================
# Generated LaTeX macros
# ============================================================

macros = (
    GEN
    / "transistor_ac_macros.tex"
)

macros.write_text(
f"""% AUTO-GENERATED -- DO NOT EDIT

\\newcommand{{\\ACFinalGainTwo}}{{{r2_180['A0_dB']:.1f}}}
\\newcommand{{\\ACFinalUGFTwo}}{{{r2_180['UGF_Hz']/1e3:.0f}}}
\\newcommand{{\\ACFinalPMTwo}}{{{r2_180['PM_deg']:.1f}}}

\\newcommand{{\\ACFinalGainFour}}{{{r4_180['A0_dB']:.1f}}}
\\newcommand{{\\ACFinalUGFFour}}{{{r4_180['UGF_Hz']/1e3:.0f}}}
\\newcommand{{\\ACFinalPMFour}}{{{r4_180['PM_deg']:.1f}}}

\\newcommand{{\\CMillerNominalFF}}{{{cap_nom_ff:.1f}}}
\\newcommand{{\\RMillerNominalK}}{{{r4_180['RZ_nom_ohm']/1e3:.1f}}}
"""
)


# ============================================================
# Generated compensation table
# ============================================================

table = (
    GEN
    / "transistor_ac_comp_table.tex"
)

table.write_text(
f"""% AUTO-GENERATED -- DO NOT EDIT

\\begin{{table}}[ht]
    \\centering
    \\caption{{Final transistor-level compensation study at
    $C_L=4~\\mathrm{{pF}}$.}}
    \\label{{tab:transistor_compensation}}

    \\begin{{tabular}}{{lccc}}
        \\hline

        $R_{{\\mathrm{{MILLER}}}}$
        & DC gain
        & UGF
        & Phase margin \\\\

        \\hline

        Short reference
        & {r4_short['A0_dB']:.1f} dB
        & {r4_short['UGF_Hz']/1e3:.1f} kHz
        & ${r4_short['PM_deg']:.1f}^\\circ$ \\\\

        19 k$\\Omega$ physical
        & {r4_19['A0_dB']:.1f} dB
        & {r4_19['UGF_Hz']/1e3:.1f} kHz
        & ${r4_19['PM_deg']:.1f}^\\circ$ \\\\

        110 k$\\Omega$ physical
        & {r4_110['A0_dB']:.1f} dB
        & {r4_110['UGF_Hz']/1e3:.1f} kHz
        & ${r4_110['PM_deg']:.1f}^\\circ$ \\\\

        180 k$\\Omega$ physical (selected)
        & {r4_180['A0_dB']:.1f} dB
        & {r4_180['UGF_Hz']/1e3:.1f} kHz
        & ${r4_180['PM_deg']:.1f}^\\circ$ \\\\

        \\hline
    \\end{{tabular}}
\\end{{table}}
"""
)


# ============================================================
# Cleanup
# ============================================================

(
    OUT
    / "_tmp_ac_case.spice"
).unlink(
    missing_ok=True
)


# ============================================================
# Final console summary
# ============================================================

print()

print(
    "Physical compensation network:"
)

print(
    f"  CMILLER = "
    f"{cap_nom_ff:.2f} fF "
    f"({cap_W:g} x "
    f"{cap_L:g} um, "
    f"MF={cap_MF:g})"
)

print(
    f"  RMILLER = "
    f"{res_base_nom/1e3:.2f} kohm "
    f"(L={res_base_L:g} um, "
    f"W=0.35 um, "
    f"mult={res_mult:g})"
)

print()

print(
    "Generated:"
)

print(
    f"  {summary}"
)

print(
    f"  {manifest}"
)

print(
    f"  {macros}"
)

print(
    f"  {table}"
)
