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
N 780 -730 780 -690 {lab=ibias_500nA}
N 1020 -690 1050 -690 {lab=Vout}
N 1460 -710 1460 -690 {lab=Vout}
N 780 -730 800 -730 {lab=ibias_500nA}
N 940 -710 1050 -710 {lab=VCM_SWEEP}
N 880 -710 880 -690 {lab=VCM_SWEEP}
N 1350 -710 1460 -710 {lab=Vout}
N 1540 -730 1540 -690 {lab=VDD}
N 1350 -730 1540 -730 {lab=VDD}
N 800 -730 860 -730 {lab=ibias_500nA}
N 880 -710 940 -710 {lab=VCM_SWEEP}
N 1020 -820 1020 -690 {lab=Vout}
N 1020 -820 1380 -820 {lab=Vout}
N 1380 -820 1380 -710 {lab=Vout}
C {/foss/designs/project_2stage_OTA/dfii/project_2stage_OTA/ota_2stage_transistor.sym} 1200 -710 0 0 {name=x1}
C {gnd.sym} 1380 -670 0 0 {name=l2 lab=0}
C {gnd.sym} 1540 -630 0 0 {name=l1 lab=0}
C {vsource.sym} 1540 -660 0 0 {name=V1 value=1.8 savecurrent=false}
C {lab_wire.sym} 1460 -730 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} 780 -630 0 0 {name=l3 lab=0}
C {isource.sym} 780 -660 0 0 {name=IBIAS value=500n}
C {capa.sym} 1460 -660 0 0 {name=CL
m=1
value=4p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1460 -630 0 0 {name=l5 lab=0}
C {lab_wire.sym} 990 -730 0 0 {name=p2 sig_type=std_logic lab=ibias_500nA}
C {lab_wire.sym} 1460 -710 0 0 {name=p3 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 990 -710 0 0 {name=p4 sig_type=std_logic lab=VCM_SWEEP}
C {code_shown.sym} 30 -850 0 0 {name=s1 only_toplevel=false value="

.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt

.control

save all

dc VCM_SRC 0 1.8 5m

* ------------------------------------------------------------
* Closed-loop tracking
* ------------------------------------------------------------

let verr = v(Vout)-v(VCM_SWEEP)
let verr_mV = 1e3*verr

* In a DC sweep, deriv(Vout) is dVout/dVCM.
* Ideal unity-follower tracking gives approximately 1 V/V.
let tracking_gain = deriv(v(Vout))

* ------------------------------------------------------------
* Useful internal headroom quantities
* ------------------------------------------------------------

let vsd_pt1 = 1.8-v(x1.vcm)

let vsd_pdiff_p = v(x1.vcm)-v(x1.out_s1)
let vsd_pdiff_n = v(x1.vcm)-v(x1.vdiode_n)

* ------------------------------------------------------------
* Plots
* ------------------------------------------------------------

plot v(VCM_SWEEP) v(Vout)

plot verr_mV

plot tracking_gain

plot v(x1.vcm) v(x1.out_s1) v(x1.vdiode_n)

plot vsd_pt1 vsd_pdiff_p vsd_pdiff_n

.endc

"}
C {gnd.sym} 880 -630 0 0 {name=l6 lab=0}
C {vsource.sym} 880 -660 0 0 {name=VCM_SRC value=0.6 savecurrent=false}
