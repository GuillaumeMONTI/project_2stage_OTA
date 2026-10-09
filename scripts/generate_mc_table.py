#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

ROOT = Path("/foss/designs/project_2stage_OTA")

CSV = ROOT / (
    "work/montecarlo/iterations/"
    "final_CC736_RZ180/mc_summary.csv"
)

OUT = ROOT / "report/generated/montecarlo_summary_table.tex"

OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

lines = []

lines.append(r"\begin{table}[H]")
lines.append(r"\centering")
lines.append(r"\caption{Monte Carlo summary for process and mismatch variations.}")
lines.append(r"\label{tab:mc_summary}")
lines.append(r"\small")
lines.append(r"\begin{tabular}{ccrrrr}")
lines.append(r"\toprule")
lines.append(
    r"$V_{DD}$ [V] & $T$ [$^\circ$C] & "
    r"$\mu(V_{OS})$ [mV] & $\sigma(V_{OS})$ [mV] & "
    r"$\mu(A_0)$ [dB] & $\sigma(A_0)$ [dB] \\"
)
lines.append(r"\midrule")

for _, r in df.iterrows():

    lines.append(
        f"{r['vdd']:.2f} & "
        f"{int(r['temp_c'])} & "
        f"{r['vos_mean_uv']/1000:+.2f} & "
        f"{r['vos_sigma_uv']/1000:.2f} & "
        f"{r['a0_mean_db']:.2f} & "
        f"{r['a0_sigma_db']:.3f} \\\\"
    )

lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")
lines.append(r"\end{table}")

OUT.write_text("\n".join(lines) + "\n")

print(f"Generated: {OUT}")
