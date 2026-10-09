# Two-Stage CMOS OTA Design in SKY130A

Open-source design and characterization of a low-power, two-stage CMOS operational transconductance amplifier (OTA) using **Xschem, ngspice, Python, SKY130A, and IIC-OSIC-TOOLS**.

The objective is to document a reproducible, specification-driven analog IC design process: starting from first-order calculations and an ideal two-stage model, then introducing transistor-level limitations, physical PDK devices, compensation, and statistical variations. The selected OTA is intended as a learning and reference design for low-power analog blocks, including PMIC and voltage-reference applications.

---

## PDF Report

### [Open the interactive PDF report](https://guillaumemonti.github.io/project_2stage_OTA/report/report_project_2stage_OTA.pdf)

[View the PDF file on GitHub](https://github.com/GuillaumeMONTI/project_2stage_OTA/blob/main/report/report_project_2stage_OTA.pdf)

The interactive version is recommended because internal section, figure, table, and reference links remain clickable.

The report contains:

- design specifications, architecture, and bias-current selection,
- first-order analog design and transistor sizing using previously characterized SKY130A MOS data,
- ideal two-stage gain, pole–zero, and Miller compensation analysis,
- transistor-level implementation with physical SKY130A MIM-capacitor and poly-resistor models,
- open-loop AC performance, slew rate, headroom estimates, and supply rejection,
- integrated noise and individual device-noise contributions,
- **45 PVT conditions** covering five process corners, three supply voltages, and three temperatures,
- **2,700 Monte Carlo simulations** combining statistical process and local mismatch models,
- iterative reduction of input-referred offset, including matching, area, and stability trade-offs.

---

## Main Results

The selected schematic-level design operates at **1.8 V** with approximately **4.0 µA** total quiescent current, including the reference bias branch.

| Parameter | Simulated result |
| --- | ---: |
| DC open-loop gain | 89.73 dB |
| Unity-gain frequency, 2 pF load | 1.184 MHz |
| Phase margin, 2 pF load | 89.04° |
| Unity-gain frequency, 4 pF load | 1.068 MHz |
| Phase margin, 4 pF load | 74.98° |
| Minimum phase margin across 45 PVT conditions | 64.69° |
| PSRR+ at 1 kHz, nominal | 99.86 dB |
| Integrated output noise, 1 Hz–1 MHz | 120.27 µV RMS |
| Input-referred offset standard deviation, nominal | 1.109 mV |

Increasing the first-stage NMOS mirror area reduced the nominal offset standard deviation from **6.125 mV to 1.109 mV**. The final nominal 3σ offset spread is **3.33 mV**, slightly above the approximately 3 mV optimization objective; that limitation is discussed in the report.

These results are from **schematic-level simulation**. Physical layout, extracted parasitics, and post-layout verification are the next steps, not completed results.

---

## Design Methodology

1. Define targets and select a two-stage PMOS-input OTA topology.
2. Derive first-order device currents, transconductances, gain, and Miller compensation.
3. Validate the idealized architecture before introducing transistor parasitics.
4. Size SKY130A MOS devices using the earlier [MOS characterization project](https://github.com/GuillaumeMONTI/project_carac_sky130A).
5. Optimize the transistor-level circuit, matching, and physical compensation network.
6. Evaluate AC, transient, noise, PSRR, PVT, and Monte Carlo performance.
7. Proceed to layout, DRC/LVS, extraction, and post-layout characterization.

---

## Tools and Environment

- **IIC-OSIC-TOOLS** with the **SKY130A** open PDK
- **Xschem** for transistor-level schematics and testbenches
- **ngspice** for circuit simulation
- **Python** for automated analysis, plots, PVT, and Monte Carlo
- **LaTeX** for the technical report
- **Magic, Netgen, and/or KLayout** for the planned physical-design verification stage

---

## Repository Structure

- `dfii/project_2stage_OTA/` — OTA schematic and symbol
- `dfii/project_2stage_OTA_sim/` — simulation testbenches
- `scripts/` — AC, PVT, Monte Carlo, noise, and figure-generation utilities
- `report/` — LaTeX source, generated tables, final figures, and compiled PDF
- `work/` — local netlists and simulation outputs (not intended for version control)
- `models/` — local PDK/model-related setup when applicable
- `.setup` — IIC project environment setup
- [`SIMULATION_WORKFLOW.md`](SIMULATION_WORKFLOW.md) — reproducible netlisting, simulation, plotting, and report flow

---

## Project Status

**Schematic-level design and characterization: completed.**

**Layout and post-layout verification: next stage.** The same repository will be extended with matching-aware layout, DRC, LVS, parasitic extraction, and post-layout comparison. No completion date is assumed.
