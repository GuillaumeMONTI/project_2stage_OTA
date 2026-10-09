#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path("/foss/designs/project_2stage_OTA")

CSV = ROOT / (
    "work/montecarlo/iterations/"
    "final_CC736_RZ180/mc_results.csv"
)

FIGDIR = ROOT / "report/figures/montecarlo"

FIGDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

df = df[df["status"] == "PASS"]

nom = df[
    (df["vdd"] == 1.80) &
    (df["temp_c"] == 27)
]

# ------------------------------------------------------------
# Offset histogram
# ------------------------------------------------------------

mu_vos = nom["vos_uv"].mean()
sigma_vos = nom["vos_uv"].std(ddof=1)

plt.figure(figsize=(6.4, 4.2))

plt.hist(
    nom["vos_uv"] / 1000.0,
    bins=25,
    edgecolor="black",
    alpha=0.75
)

plt.axvline(
    mu_vos / 1000.0,
    linestyle="--",
    linewidth=1.4,
    label=fr"$\mu$ = {mu_vos/1000:.2f} mV"
)

plt.axvline(
    (mu_vos - 3*sigma_vos) / 1000.0,
    linestyle=":",
    linewidth=1.2,
    label=fr"$\mu \pm 3\sigma$ = {3*sigma_vos/1000:.2f} mV"
)

plt.axvline(
    (mu_vos + 3*sigma_vos) / 1000.0,
    linestyle=":",
    linewidth=1.2
)

plt.xlabel(r"Input-referred offset $V_{OS}$ [mV]")
plt.ylabel("Samples")
plt.title(r"Monte Carlo -- $V_{DD}=1.8$ V, $T=27^\circ$C")
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()

plt.savefig(
    FIGDIR / "mc_vos_nominal.pdf",
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Gain histogram
# ------------------------------------------------------------

mu_a0 = nom["a0_db"].mean()
sigma_a0 = nom["a0_db"].std(ddof=1)

plt.figure(figsize=(6.4, 4.2))

plt.hist(
    nom["a0_db"],
    bins=25,
    edgecolor="black",
    alpha=0.75
)

plt.axvline(
    mu_a0 - 3*sigma_a0,
    linestyle=":",
    linewidth=1.2,
    label=fr"$3\sigma$ = {3*sigma_a0:.2f} dB"
)

plt.axvline(
    mu_a0 + 3*sigma_a0,
    linestyle=":",
    linewidth=1.2
)

plt.xlabel(r"DC open-loop gain $A_0$ [dB]")
plt.ylabel("Samples")
plt.title(r"Monte Carlo -- $V_{DD}=1.8$ V, $T=27^\circ$C")
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()

plt.savefig(
    FIGDIR / "mc_gain_nominal.pdf",
    bbox_inches="tight"
)

plt.close()

print("Generated:")
print(FIGDIR / "mc_vos_nominal.pdf")
print(FIGDIR / "mc_gain_nominal.pdf")
