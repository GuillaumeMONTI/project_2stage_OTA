v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1410 -690 1440 -690 {lab=0}
N 1440 -690 1440 -670 {lab=0}
N 860 -730 1050 -730 {lab=ibias_500nA}
N 840 -730 840 -690 {lab=ibias_500nA}
N 1020 -690 1050 -690 {lab=Vin_N}
N 1520 -710 1520 -690 {lab=Vout}
N 1440 -800 1440 -710 {lab=Vout}
N 840 -730 860 -730 {lab=ibias_500nA}
N 940 -710 1050 -710 {lab=Vin_P}
N 940 -710 940 -690 {lab=Vin_P}
N 1020 -800 1020 -690 {lab=Vin_N}
N 1410 -710 1520 -710 {lab=Vout}
N 1600 -730 1600 -690 {lab=VDD}
N 1410 -730 1600 -730 {lab=VDD}
N 1020 -800 1030 -800 {lab=Vin_N}
N 1090 -800 1100 -800 {lab=Vin_N}
N 1100 -800 1200 -800 {lab=Vin_N}
N 1260 -800 1440 -800 {lab=Vout}
N 1030 -800 1090 -800 {lab=Vin_N}
N 1050 -730 1110 -730 {lab=ibias_500nA}
N 1050 -710 1110 -710 {lab=Vin_P}
N 1050 -690 1110 -690 {lab=Vin_N}
N 1020 -690 1020 -670 {lab=Vin_N}
C {/foss/designs/project_2stage_OTA/dfii/project_2stage_OTA/ota_2stage_transistor.sym} 1260 -710 0 0 {name=x1}
C {gnd.sym} 1440 -670 0 0 {name=l2 lab=0}
C {gnd.sym} 1600 -630 0 0 {name=l1 lab=0}
C {vsource.sym} 1600 -660 0 0 {name=V1 value=1.8 savecurrent=false}
C {lab_wire.sym} 1520 -730 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {gnd.sym} 840 -630 0 0 {name=l3 lab=0}
C {isource.sym} 840 -660 0 0 {name=IBIAS value=500n}
C {gnd.sym} 940 -630 0 0 {name=l4 lab=0}
C {vsource.sym} 940 -660 0 0 {name=Vin_P value="DC 0.6 AC 1" savecurrent=false}
C {capa.sym} 1520 -660 0 0 {name=CL
m=1
value=4p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1520 -630 0 0 {name=l5 lab=0}
C {lab_wire.sym} 990 -730 0 0 {name=p2 sig_type=std_logic lab=ibias_500nA}
C {lab_wire.sym} 1520 -710 0 0 {name=p3 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 990 -710 0 0 {name=p4 sig_type=std_logic lab=Vin_P}
C {code_shown.sym} 30 -850 0 0 {name=s1 only_toplevel=false value="

.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt

.control

set wr_singlescale
set wr_vecnames

ac dec 200 1 100Meg

let vid       = v(Vin_P)-v(Vin_N)
let aol       = v(Vout)/vid
let gain_db   = db(aol)
let phase_deg = 180/PI*cph(aol)

meas ac A0_dB FIND gain_db AT=1
meas ac UGF WHEN gain_db=0 CROSS=1
meas ac PHASE_UGF FIND phase_deg WHEN gain_db=0 CROSS=1

let PM = 180 + PHASE_UGF

print A0_dB
print UGF
print PHASE_UGF
print PM

plot gain_db
plot phase_deg

.endc
"}
C {ind.sym} 1230 -800 3 1 {name=LDC
m=1
value=1G
footprint=1206
device=inductor}
C {capa.sym} 1020 -640 0 0 {name=CAC
m=1
value=1
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1020 -610 0 0 {name=l6 lab=0}
C {lab_wire.sym} 1130 -800 0 0 {name=p5 sig_type=std_logic lab=Vin_N}
