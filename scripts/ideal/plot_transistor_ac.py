import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]

WORK = ROOT / "work" / "transistor"
OUT = ROOT / "report" / "figures" / "transistor" / "ac"

OUT.mkdir(parents=True, exist_ok=True)


def read_summary():
    with open(WORK / "ac_summary.csv") as f:
        return list(csv.DictReader(f))


def find_case(rows, cl_pf, rz_mode):
    for row in rows:
        if (
            abs(float(row["CL_pF"]) - cl_pf) < 1e-9
            and row["RZ_mode"] == rz_mode
        ):
            return row

    raise RuntimeError(
        f"Missing AC case: CL={cl_pf} pF, RZ={rz_mode}"
    )


def load_case(row):
    data = np.loadtxt(
        WORK / row["filename"],
        skiprows=1,
    )

    return (
        data[:, 0],
        data[:, 1],
        data[:, 2],
    )


rows = read_summary()


# ============================================================
# Compensation comparison -- CL = 4 pF
# ============================================================

cases = [
    (
        find_case(rows, 4.0, "SHORT"),
        "No series resistor",
    ),
    (
        find_case(rows, 4.0, "19k"),
        r"$R_z \approx 19$ k$\Omega$",
    ),
    (
        find_case(rows, 4.0, "110k"),
        r"$R_z \approx 110$ k$\Omega$",
    ),
]

fig, (ax_gain, ax_phase) = plt.subplots(
    2,
    1,
    figsize=(7.0, 6.5),
    sharex=True,
)

for row, label in cases:

    freq, gain, phase = load_case(row)

    ax_gain.semilogx(
        freq,
        gain,
        label=label,
    )

    ax_phase.semilogx(
        freq,
        phase,
        label=label,
    )


ax_gain.axhline(
    0,
    linewidth=0.8,
)

ax_gain.set_ylabel(
    "Open-loop gain (dB)"
)

ax_gain.grid(
    True,
    which="both",
    alpha=0.3,
)

ax_gain.legend(
    fontsize=8,
)


ax_phase.axhline(
    -180,
    linewidth=0.8,
)

ax_phase.set_xlabel(
    "Frequency (Hz)"
)

ax_phase.set_ylabel(
    "Phase (deg)"
)

ax_phase.grid(
    True,
    which="both",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    OUT
    / "transistor_ac_compensation_comparison.pdf",
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# Load comparison -- physical Rz ~= 110 kOhm
# ============================================================

cases = [
    (
        find_case(rows, 2.0, "110k"),
        r"$C_L = 2$ pF",
    ),
    (
        find_case(rows, 4.0, "110k"),
        r"$C_L = 4$ pF",
    ),
]

fig, (ax_gain, ax_phase) = plt.subplots(
    2,
    1,
    figsize=(7.0, 6.5),
    sharex=True,
)

for row, label in cases:

    freq, gain, phase = load_case(row)

    ax_gain.semilogx(
        freq,
        gain,
        label=label,
    )

    ax_phase.semilogx(
        freq,
        phase,
        label=label,
    )


ax_gain.axhline(
    0,
    linewidth=0.8,
)

ax_gain.set_ylabel(
    "Open-loop gain (dB)"
)

ax_gain.grid(
    True,
    which="both",
    alpha=0.3,
)

ax_gain.legend(
    fontsize=8,
)


ax_phase.axhline(
    -180,
    linewidth=0.8,
)

ax_phase.set_xlabel(
    "Frequency (Hz)"
)

ax_phase.set_ylabel(
    "Phase (deg)"
)

ax_phase.grid(
    True,
    which="both",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    OUT
    / "transistor_ac_load_comparison.pdf",
    bbox_inches="tight",
)

plt.close(fig)

print("Generated:")
print(
    OUT
    / "transistor_ac_compensation_comparison.pdf"
)
print(
    OUT
    / "transistor_ac_load_comparison.pdf"
)
