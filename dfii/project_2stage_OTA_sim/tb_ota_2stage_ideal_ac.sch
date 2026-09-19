v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1150 -800 1150 -770 {lab=Vout}
N 1070 -800 1150 -800 {lab=Vout}
N 1070 -820 1150 -820 {lab=out_s1}
N 740 -800 770 -800 {lab=0}
N 690 -820 690 -770 {lab=Vin_P}
N 690 -820 770 -820 {lab=Vin_P}
C {/foss/designs/project_2stage_OTA/dfii/project_2stage_OTA/ota_2stage_ideal.sym} 920 -810 0 0 {name=x1}
C {gnd.sym} 740 -800 0 0 {name=l1 lab=0}
C {gnd.sym} 1150 -710 0 0 {name=l2 lab=0}
C {capa.sym} 1150 -740 0 0 {name=CL
m=1
value=4p
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} 1130 -800 0 0 {name=p1 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 1130 -820 0 0 {name=p2 sig_type=std_logic lab=out_s1}
C {gnd.sym} 690 -710 0 0 {name=l3 lab=0}
C {vsource.sym} 690 -740 0 0 {name=V1 value="DC 0 AC 1" savecurrent=false}
C {code_shown.sym} 10 -1010 0 0 {name=s1 only_toplevel=false value="

.control

set wr_singlescale
set wr_vecnames

ac dec 200 1 100Meg

let aol       = v(Vout)/v(Vin_P)
let gain_db   = db(aol)
let phase_deg = 180/PI*cph(aol)

* ------------------------------------------------------------
* Automatic measurements
* ------------------------------------------------------------

meas ac A0_dB FIND gain_db AT=1

meas ac UGF WHEN gain_db=0 CROSS=1

meas ac PHASE_UGF FIND phase_deg WHEN gain_db=0 CROSS=1

let PM = 180 + PHASE_UGF

print A0_dB
print UGF
print PHASE_UGF
print PM

* ------------------------------------------------------------
* Save numerical data for Python/report
* ------------------------------------------------------------

wrdata ideal/ac_CL4p_Rz0.dat gain_db phase_deg

* Temporary interactive plots
plot gain_db
plot phase_deg

.endc
"}
C {lab_wire.sym} 740 -820 0 0 {name=p3 sig_type=std_logic lab=Vin_P}
