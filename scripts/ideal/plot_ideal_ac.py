import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WORK = ROOT / "work" / "ideal"
OUT  = ROOT / "report" / "figures" / "ideal" / "ac"

OUT.mkdir(parents=True, exist_ok=True)


CASES = [
    (
        WORK / "ac_CL2p_Rz0.dat",
        r"$C_L=2$ pF, $R_z=0$"
    ),
    (
        WORK / "ac_CL4p_Rz0.dat",
        r"$C_L=4$ pF, $R_z=0$"
    ),
    (
        WORK / "ac_CL4p_Rz18k4.dat",
        r"$C_L=4$ pF, $R_z=18.4$ k$\Omega$"
    ),
    (
        WORK / "ac_CL4p_Rz110k.dat",
        r"$C_L=4$ pF, $R_z=110$ k$\Omega$"
    ),
]


def load_wrdata(path):
    data = np.loadtxt(path, skiprows=1)

    freq = data[:, 0]
    gain = data[:, 1]
    phase = data[:, 2]

    return freq, gain, phase


fig, (ax_gain, ax_phase) = plt.subplots(
    2,
    1,
    figsize=(7.0, 6.5),
    sharex=True
)

for path, label in CASES:

    freq, gain, phase = load_wrdata(path)

    ax_gain.semilogx(freq, gain, label=label)
    ax_phase.semilogx(freq, phase, label=label)


# ------------------------------------------------------------
# Magnitude
# ------------------------------------------------------------

ax_gain.axhline(0, linewidth=0.8)
ax_gain.set_ylabel("Open-loop gain (dB)")
ax_gain.grid(True, which="both", alpha=0.3)
ax_gain.legend(fontsize=8)


# ------------------------------------------------------------
# Phase
# ------------------------------------------------------------

ax_phase.axhline(-180, linewidth=0.8)
ax_phase.set_xlabel("Frequency (Hz)")
ax_phase.set_ylabel("Phase (deg)")
ax_phase.grid(True, which="both", alpha=0.3)


fig.tight_layout()

fig.savefig(
    OUT / "ideal_ac_compensation_comparison.pdf",
    bbox_inches="tight"
)

plt.close(fig)
