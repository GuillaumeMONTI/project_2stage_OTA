# Two-Stage OTA Design in SKY130A

Design and characterization of a classical two-stage CMOS OTA using the
SKY130A open-source PDK.

The project follows a specification-driven analog design flow:

1. ideal architectural model,
2. first-order analytical design,
3. transistor-level sizing using previously extracted SKY130A device data,
4. simulation and design iteration,
5. PVT and non-ideal analysis.

The intended application is a low-power, high-gain OTA representative of
PMIC and voltage-reference analog design.

## Environment

- IIC-OSIC-TOOLS
- SKY130A open PDK
- Xschem
- ngspice
- Python
- LaTeX

## Design flow

The project starts from an ideal two-stage model to establish the required
gain, bandwidth, compensation and stability.

The transistor-level implementation will then reuse the device
characterization obtained in
[`project_carac_sky130A`](https://github.com/GuillaumeMONTI/project_carac_sky130A),
including g<sub>m</sub>/I<sub>D</sub>, I<sub>D</sub>/W, intrinsic gain,
V<sub>TH</sub> and V<sub>DSAT</sub> data.

## Report

[View the current PDF report](report/report_project_2stage_OTA.pdf)

The interactive GitHub Pages version will eventually be available at:

`https://guillaumemonti.github.io/project_2stage_OTA/report/report_project_2stage_OTA.pdf`

## Repository structure

- `dfii/project_2stage_OTA/` — design schematics
- `dfii/project_2stage_OTA_sim/` — simulation testbenches
- `work/` — generated simulation data and netlists
- `scripts/` — Python post-processing and project utilities
- `report/` — LaTeX report and final figures
- `models/` — local model-generation area when required

## Status

Project environment initialized. OTA specifications and architecture are
currently being defined.

## Reproducible Simulation Flow

See [SIMULATION_WORKFLOW.md](SIMULATION_WORKFLOW.md) for the automated
ngspice regression, plot-generation and report-generation workflow.
