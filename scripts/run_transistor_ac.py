from pathlib import Path
import subprocess
import hashlib
import re
import csv
import math

ROOT = Path(__file__).resolve().parents[1]

WORK = ROOT / "work"
NETLIST = WORK / "tb_ota_2stage_ac.spice"

OUT = WORK / "transistor"
GEN = ROOT / "report" / "generated"

OUT.mkdir(parents=True, exist_ok=True)
GEN.mkdir(parents=True, exist_ok=True)


# ============================================================
# AC sweep definition
# ============================================================

CL_CASES = [
    (2.0, "2p"),
    (4.0, "4p"),
]

RZ_CASES = [
    (0.0,    "1m"),     # ~0 ohm, avoid exact zero
    (19e3,   "19k"),
    (110e3,  "110k"),
]


# ============================================================
# Helpers
# ============================================================

def parse_spice_value(s):
    s = s.strip()

    suffixes = {
        "t": 1e12,
        "g": 1e9,
        "meg": 1e6,
        "k": 1e3,
        "m": 1e-3,
        "u": 1e-6,
        "n": 1e-9,
        "p": 1e-12,
        "f": 1e-15,
    }

    m = re.fullmatch(
        r"([+-]?[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?)(meg|[tgkmunpf]?)",
        s,
        re.I,
    )

    if not m:
        raise ValueError(f"Cannot parse SPICE value: {s}")

    value = float(m.group(1))
    suffix = m.group(2).lower()

    return value * suffixes.get(suffix, 1.0)


def number_tag(x):
    return f"{x:g}".replace(".", "p")


def remove_control(text):
    return re.sub(
        r"(?ms)^\s*\.control\b.*?^\s*\.endc\s*\n?",
        "",
        text,
    )


def replace_component_value(text, name, value):
    pattern = rf"(?mi)^({re.escape(name)}\s+\S+\s+\S+\s+)\S+"

    new_text, count = re.subn(
        pattern,
        rf"\g<1>{value}",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError(f"Could not uniquely replace {name}")

    return new_text


def insert_control(text, control):
    matches = list(re.finditer(r"(?mi)^\s*\.end\s*$", text))

    if matches:
        pos = matches[-1].start()
        return text[:pos] + control + "\n" + text[pos:]

    return text + "\n" + control + "\n.end\n"


def load_wrdata(path):
    rows = []

    with open(path) as f:
        for line in f:
            if line.lstrip().startswith("frequency"):
                continue

            parts = line.split()

            if len(parts) >= 3:
                try:
                    rows.append(tuple(map(float, parts[:3])))
                except ValueError:
                    pass

    if not rows:
        raise RuntimeError(f"No numerical data found in {path}")

    return rows


def extract_metrics(path):
    rows = load_wrdata(path)

    f = [r[0] for r in rows]
    g = [r[1] for r in rows]
    p = [r[2] for r in rows]

    # Low-frequency gain at first point (~1 Hz)
    a0 = g[0]

    crossing = None

    for i in range(len(g) - 1):
        if g[i] >= 0 and g[i + 1] < 0:
            crossing = i
            break

    if crossing is None:
        raise RuntimeError(f"No 0-dB crossing in {path}")

    i = crossing

    x1 = math.log10(f[i])
    x2 = math.log10(f[i + 1])

    frac = (0.0 - g[i]) / (g[i + 1] - g[i])

    xu = x1 + frac * (x2 - x1)

    ugf = 10 ** xu

    phase = p[i] + frac * (p[i + 1] - p[i])

    pm = 180.0 + phase

    return a0, ugf, phase, pm


def instance_blocks(text):
    wanted = (
        "XPDIFF",
        "XNLOAD",
        "XPTAIL",
        "CMILLER",
        "RMILLER",
        "CL ",
    )

    lines = text.splitlines()
    out = []

    i = 0

    while i < len(lines):
        line = lines[i]

        if line.upper().startswith(wanted):
            block = [line]

            j = i + 1

            while j < len(lines) and lines[j].lstrip().startswith("+"):
                block.append(lines[j])
                j += 1

            out.extend(block)
            i = j
        else:
            i += 1

    return out


# ============================================================
# Load current Xschem netlist
# ============================================================

if not NETLIST.exists():
    raise SystemExit(
        "ERROR: tb_ota_2stage_ac.spice not found.\n"
        "Open Xschem and regenerate the AC testbench netlist first."
    )

base = NETLIST.read_text()

cm_match = re.search(
    r"(?mi)^CMILLER\s+\S+\s+\S+\s+(\S+)",
    base,
)

if not cm_match:
    raise SystemExit("ERROR: CMILLER not found in netlist.")

cm_spice = cm_match.group(1)
cm_pf = parse_spice_value(cm_spice) / 1e-12

cm_tag = f"{number_tag(cm_pf)}pF"


# ============================================================
# Delete old automatically generated AC data
# ============================================================

for p in OUT.glob("ac_CL*_CM*_RZ*.dat"):
    p.unlink()

for p in OUT.glob("ac_CL*_CM*_RZ*.log"):
    p.unlink()


# ============================================================
# Run all cases
# ============================================================

results = []

for cl_pf, cl_spice in CL_CASES:

    for rz_ohm, rz_spice in RZ_CASES:

        if rz_ohm == 0:
            rz_tag = "0"
        else:
            rz_tag = f"{number_tag(rz_ohm / 1e3)}k"

        filename = (
            f"ac_CL{number_tag(cl_pf)}pF_"
            f"CM{cm_tag}_"
            f"RZ{rz_tag}.dat"
        )

        logfile = filename.replace(".dat", ".log")

        text = remove_control(base)

        text = replace_component_value(
            text,
            "CL",
            cl_spice,
        )

        text = replace_component_value(
            text,
            "RMILLER",
            rz_spice,
        )

        control = f"""
.control

set wr_singlescale
set wr_vecnames

ac dec 200 1 100Meg

let vid       = v(Vin_P)-v(Vin_N)
let aol       = v(Vout)/vid
let gain_db   = db(aol)
let phase_deg = 180/PI*cph(aol)

wrdata transistor/{filename} gain_db phase_deg

quit

.endc
"""

        text = insert_control(text, control)

        temp_netlist = OUT / "_tmp_ac_case.spice"
        temp_netlist.write_text(text)

        proc = subprocess.run(
            ["ngspice", "-b", str(temp_netlist)],
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        (OUT / logfile).write_text(proc.stdout)

        dat_path = OUT / filename

        if not dat_path.exists():
            print(proc.stdout)
            raise RuntimeError(f"Simulation failed: {filename}")

        a0, ugf, phase, pm = extract_metrics(dat_path)

        results.append({
            "filename": filename,
            "CL_pF": cl_pf,
            "CM_pF": cm_pf,
            "RZ_ohm": rz_ohm,
            "A0_dB": a0,
            "UGF_Hz": ugf,
            "phase_UGF_deg": phase,
            "PM_deg": pm,
        })

        print(
            f"{filename:<45} "
            f"A0={a0:6.2f} dB  "
            f"UGF={ugf/1e3:8.1f} kHz  "
            f"PM={pm:6.2f} deg"
        )


# ============================================================
# Summary CSV
# ============================================================

summary = OUT / "ac_summary.csv"

with open(summary, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=results[0].keys(),
    )

    writer.writeheader()
    writer.writerows(results)


# ============================================================
# Manifest: bind results to CURRENT transistor netlist
# ============================================================

digest = hashlib.sha256(base.encode()).hexdigest()

manifest = OUT / "ac_manifest.txt"

with open(manifest, "w") as f:

    f.write(f"Netlist SHA256: {digest}\n")
    f.write(f"CMILLER: {cm_spice}\n\n")

    f.write("Relevant current netlist instances:\n")
    f.write("-----------------------------------\n")

    for line in instance_blocks(base):
        f.write(line + "\n")


# ============================================================
# Helpers for generated LaTeX
# ============================================================

def get_result(cl, rz):
    for r in results:
        if r["CL_pF"] == cl and r["RZ_ohm"] == rz:
            return r

    raise RuntimeError(f"Missing case CL={cl}, RZ={rz}")


r2_110 = get_result(2.0, 110e3)
r4_0   = get_result(4.0, 0.0)
r4_19  = get_result(4.0, 19e3)
r4_110 = get_result(4.0, 110e3)


# ============================================================
# Generated LaTeX macros
# ============================================================

macros = GEN / "transistor_ac_macros.tex"

macros.write_text(
f"""% AUTO-GENERATED -- DO NOT EDIT

\\newcommand{{\\ACFinalGainTwo}}{{{r2_110['A0_dB']:.1f}}}
\\newcommand{{\\ACFinalUGFTwo}}{{{r2_110['UGF_Hz']/1e3:.0f}}}
\\newcommand{{\\ACFinalPMTwo}}{{{r2_110['PM_deg']:.1f}}}

\\newcommand{{\\ACFinalGainFour}}{{{r4_110['A0_dB']:.1f}}}
\\newcommand{{\\ACFinalUGFFour}}{{{r4_110['UGF_Hz']/1e3:.0f}}}
\\newcommand{{\\ACFinalPMFour}}{{{r4_110['PM_deg']:.1f}}}
"""
)


# ============================================================
# Generated compensation table
# ============================================================

table = GEN / "transistor_ac_comp_table.tex"

table.write_text(
f"""% AUTO-GENERATED -- DO NOT EDIT

\\begin{{table}}[ht]
    \\centering
    \\caption{{Final transistor-level compensation study at
    $C_L=4~\\mathrm{{pF}}$.}}
    \\label{{tab:transistor_compensation}}
    \\begin{{tabular}}{{lccc}}
        \\hline
        $R_{{\\mathrm{{MILLER}}}}$ & DC gain & UGF & Phase margin \\\\
        \\hline
        $\\approx0~\\Omega$ &
        {r4_0['A0_dB']:.1f} dB &
        {r4_0['UGF_Hz']/1e3:.1f} kHz &
        ${r4_0['PM_deg']:.1f}^\\circ$ \\\\

        19 k$\\Omega$ &
        {r4_19['A0_dB']:.1f} dB &
        {r4_19['UGF_Hz']/1e3:.1f} kHz &
        ${r4_19['PM_deg']:.1f}^\\circ$ \\\\

        110 k$\\Omega$ &
        {r4_110['A0_dB']:.1f} dB &
        {r4_110['UGF_Hz']/1e3:.1f} kHz &
        ${r4_110['PM_deg']:.1f}^\\circ$ \\\\
        \\hline
    \\end{{tabular}}
\\end{{table}}
"""
)

print()
print("Generated:")
print(f"  {summary}")
print(f"  {manifest}")
print(f"  {macros}")
print(f"  {table}")

(OUT / "_tmp_ac_case.spice").unlink(missing_ok=True)
