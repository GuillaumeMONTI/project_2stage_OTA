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
N 1020 -690 1050 -690 {lab=Vout}
N 1460 -710 1460 -690 {lab=Vout}
N 1020 -800 1380 -800 {lab=Vout}
N 1380 -800 1380 -710 {lab=Vout}
N 840 -730 860 -730 {lab=ibias_500nA}
N 940 -710 1050 -710 {lab=Vin_P}
N 940 -710 940 -690 {lab=Vin_P}
N 1020 -800 1020 -690 {lab=Vout}
N 1350 -710 1460 -710 {lab=Vout}
N 1540 -730 1540 -690 {lab=VDD}
N 1350 -730 1540 -730 {lab=VDD}
C {/foss/designs/project_2stage_OTA/dfii/project_2stage_OTA/ota_2stage_transistor.sym} 1200 -710 0 0 {name=x1}
C {gnd.sym} 1380 -670 0 0 {name=l2 lab=0}
C {gnd.sym} 1540 -630 0 0 {name=l1 lab=0}
C {vsource.sym} 1540 -660 0 0 {name=V1 value=1.8 savecurrent=false}
C {lab_wire.sym} 1460 -730 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} 840 -630 0 0 {name=l3 lab=0}
C {isource.sym} 840 -660 0 0 {name=IBIAS value=500n}
C {gnd.sym} 940 -630 0 0 {name=l4 lab=0}
C {vsource.sym} 940 -660 0 0 {name=Vin_P value="PULSE(0.45 0.75 5u 1n 1n 10u 20u)" savecurrent=false}
C {capa.sym} 1460 -660 0 0 {name=CL
m=1
value=4p
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

tran 2n 30u

let dvout_dt = deriv(v(Vout))*1e-6

plot dvout_dt xlimit 4.9u 6u ylimit -0.2 1

plot dvout_dt xlimit 14.9u 16u ylimit -1 0.2

meas tran sr_rise_mid FIND dvout_dt WHEN v(Vout)=0.60 RISE=1
meas tran sr_fall_mid FIND dvout_dt WHEN v(Vout)=0.60 FALL=1

print sr_rise_mid
print sr_fall_mid

* Rising transition: 0.5 V -> 0.7 V
* 20 % = 0.54 V
* 80 % = 0.66 V

meas tran tr20 WHEN v(Vout)=0.51 RISE=1
meas tran tr80 WHEN v(Vout)=0.69 RISE=1

let sr_rise = 0.18/(tr80-tr20)*1e-6

meas tran tf80 WHEN v(Vout)=0.69 FALL=1
meas tran tf20 WHEN v(Vout)=0.51 FALL=1

let sr_fall = 0.18/(tf20-tf80)*1e-6

print tr20
print tr80
print sr_rise

print tf80
print tf20
print sr_fall

plot v(Vin_P) v(Vout)

.endc

"}
