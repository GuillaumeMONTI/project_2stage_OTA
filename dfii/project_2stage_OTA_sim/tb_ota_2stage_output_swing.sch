v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1350 -690 1380 -690 {lab=0}
N 1380 -690 1380 -670 {lab=0}
N 860 -730 1050 -730 {lab=ibias_500nA}
N 840 -730 840 -690 {lab=ibias_500nA}
N 1020 -690 1050 -690 {lab=Vin_N}
N 1460 -710 1460 -690 {lab=Vout}
N 840 -730 860 -730 {lab=ibias_500nA}
N 920 -710 1050 -710 {lab=Vin_P}
N 920 -710 920 -690 {lab=Vin_P}
N 1350 -710 1460 -710 {lab=Vout}
N 1540 -730 1540 -690 {lab=VDD}
N 1350 -730 1540 -730 {lab=VDD}
N 1000 -690 1020 -690 {lab=Vin_N}
C {/foss/designs/project_2stage_OTA/dfii/project_2stage_OTA/ota_2stage_transistor.sym} 1200 -710 0 0 {name=x1}
C {gnd.sym} 1380 -670 0 0 {name=l2 lab=0}
C {gnd.sym} 1540 -630 0 0 {name=l1 lab=0}
C {vsource.sym} 1540 -660 0 0 {name=V1 value=1.8 savecurrent=false}
C {lab_wire.sym} 1460 -730 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} 840 -630 0 0 {name=l3 lab=0}
C {isource.sym} 840 -660 0 0 {name=IBIAS value=500n}
C {gnd.sym} 920 -630 0 0 {name=l4 lab=0}
C {vsource.sym} 920 -660 0 0 {name=VIN_P_SRC value=0.6 savecurrent=false}
C {capa.sym} 1460 -660 0 0 {name=CL
m=1
value=2p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1460 -630 0 0 {name=l5 lab=0}
C {lab_wire.sym} 990 -730 0 0 {name=p2 sig_type=std_logic lab=ibias_500nA}
C {lab_wire.sym} 1460 -710 0 0 {name=p3 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 990 -710 0 0 {name=p4 sig_type=std_logic lab=Vin_P}
C {code_shown.sym} 30 -850 0 0 {name=s1 only_toplevel=false value="

.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt

.control

save all

* ------------------------------------------------------------
* Open-loop DC differential sweep
*
* Vin_N fixed at 0.600 V
* Vin_P swept +/-10 mV around it
* ------------------------------------------------------------

dc VIN_P_SRC 0.590 0.610 2u

* Differential input
let vid = v(Vin_P)-v(Vin_N)
let vid_mV = 1e3*vid

* Output headroom from each rail
let headroom_low  = v(Vout)
let headroom_high = 1.8-v(Vout)

let vdsat_pt2 = abs(@m.x1.xptail_2.msky130_fd_pr__pfet_01v8[vdsat])
let vdsat_n2 = abs(@m.x1.xnload_2.msky130_fd_pr__nfet_01v8[vdsat])

* Second-stage saturation margins

let sat_margin_n2  = v(Vout)-vdsat_n2
let sat_margin_pt2 = 1.8-v(Vout)-vdsat_pt2

plot sat_margin_n2 sat_margin_pt2

meas dc vout_linear_min FIND v(Vout) WHEN sat_margin_n2=0 RISE=1

meas dc vout_linear_max FIND v(Vout) WHEN sat_margin_pt2=0 FALL=1

print vout_linear_min
print vout_linear_max

* ------------------------------------------------------------
* Basic output-swing measurements
* ------------------------------------------------------------

meas dc vout_min MIN v(Vout)
meas dc vout_max MAX v(Vout)

print vout_min
print vout_max

* ------------------------------------------------------------
* Plots
* ------------------------------------------------------------

plot v(Vout)

plot v(Vout) vs vid_mV

plot headroom_low headroom_high

plot v(x1.out_s1) v(x1.vcm)

.endc
"}
C {gnd.sym} 1000 -630 0 0 {name=l6 lab=0}
C {vsource.sym} 1000 -660 0 0 {name=VIN_N_SRC value=0.6 savecurrent=false}
C {lab_wire.sym} 1040 -690 0 0 {name=p5 sig_type=std_logic lab=Vin_N}
