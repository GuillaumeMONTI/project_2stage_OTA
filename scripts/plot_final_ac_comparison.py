#!/usr/bin/env python3
"""Plot the final 4-pF Miller-resistor comparison from ngspice wrdata data.

Run from the project root after scripts/run_transistor_ac.py has generated
work/transistor/ac_CL4p_*_RZ<mode>.dat. Requires numpy and matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "work" / "transistor"
OUTPUT = ROOT / "report" / "figures" / "transistor" / "ac" / "transistor_ac_compensation_comparison.pdf"

CASES = [
    ("SHORT", "Short reference"),
    ("19k", r"$R_Z=19\,\mathrm{k}\Omega$"),
    ("110k", r"$R_Z=110\,\mathrm{k}\Omega$"),
    ("180k", r"$R_Z=180\,\mathrm{k}\Omega$ (selected)"),
]

def load_curve(mode):
    # Exact CM value prevents accidentally loading historical 800-fF files.
    source = DATA / f"ac_CL4pF_CM736p44fF_RZ{mode}.dat"
    if not source.is_file():
        raise RuntimeError(f"Missing AC data file: {source}")
    arr = np.loadtxt(source, comments=("#", "*"), skiprows=1)
    if arr.ndim == 1:
        arr = arr.reshape((1, -1))
    n = arr.shape[1]
    # ngspice wrdata normally repeats the frequency column for each vector:
    #   two vectors -> [frequency, gain_dB, frequency, phase]
    #   three vectors -> [frequency, frequency, frequency, gain_dB,
    #                     frequency, phase]
    if n == 4:
        frequency, gain_db, phase = arr[:, 0], arr[:, 1], arr[:, 3]
    elif n == 6:
        frequency, gain_db, phase = arr[:, 0], arr[:, 3], arr[:, 5]
    elif n == 3:
        frequency, gain_db, phase = arr[:, 0], arr[:, 1], arr[:, 2]
    else:
        raise RuntimeError(
            f"Unexpected {n}-column data format in {source}. "
            f"Inspect with: head -3 {source}"
        )
    good = np.isfinite(frequency) & np.isfinite(gain_db) & np.isfinite(phase) & (frequency > 0)
    frequency, gain_db, phase = frequency[good], gain_db[good], phase[good]
    if len(frequency) < 2:
        raise RuntimeError(f"Not enough valid AC points in {source}")
    order = np.argsort(frequency)
    frequency, gain_db, phase = frequency[order], gain_db[order], phase[order]
    # Ngspice may export phase in radians. Convert if the angular magnitude
    # is consistent with radians, then unwrap to remove +/-180 deg jumps.
    if np.max(np.abs(phase)) < 7.0:
        phase = np.rad2deg(phase)
    phase = np.rad2deg(np.unwrap(np.deg2rad(phase)))
    return frequency, gain_db, phase


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig, (axg, axp) = plt.subplots(2, 1, figsize=(8.1, 6.5), sharex=True)
    for mode, label in CASES:
        f, gain, phase = load_curve(mode)
        style = {"linewidth": 2.2} if mode == "180k" else {"linewidth": 1.4}
        line, = axg.semilogx(f, gain, label=label, **style)
        axp.semilogx(f, phase, color=line.get_color(), **style)
    axg.axhline(0, color="0.45", linewidth=0.8, linestyle="--")
    axp.axhline(-180, color="0.45", linewidth=0.8, linestyle="--")
    axg.set_ylabel("Open-loop gain (dB)")
    axp.set_ylabel("Phase (deg)")
    axp.set_xlabel("Frequency (Hz)")
    axg.legend(loc="best", fontsize=9)
    for ax in (axg, axp):
        ax.grid(True, which="both", alpha=0.2)
    fig.suptitle(r"Transistor-level Miller compensation ($C_L=4\,\mathrm{pF}$)")
    fig.tight_layout()
    fig.savefig(OUTPUT, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {OUTPUT}")

if __name__ == "__main__":
    main()
