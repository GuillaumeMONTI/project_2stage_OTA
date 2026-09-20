# Simulation and Report Generation Workflow

This project uses:

- Xschem for schematic capture and netlist generation
- ngspice inside IIC-OSIC-TOOLS for circuit simulation
- Python on the Ubuntu host for post-processing and vector PDF generation
- LaTeX for the final technical report

Simulation data under `work/` are temporary and are not version-controlled.

## Transistor-Level AC Regression

Source testbench:

`dfii/project_2stage_OTA_sim/tb_ota_2stage_ac.sch`

Generated netlist:

`work/tb_ota_2stage_ac.spice`

### 1. Regenerate the netlist

After modifying the OTA or the AC testbench:

1. Save the schematic.
2. Open `tb_ota_2stage_ac.sch`.
3. Generate the SPICE netlist from Xschem.

No `.dat` filename shall be edited manually.

### 2. Run the AC regression

Inside IIC-OSIC-TOOLS:

```bash
cd /foss/designs/project_2stage_OTA
source .setup
python3 scripts/run_transistor_ac.py
