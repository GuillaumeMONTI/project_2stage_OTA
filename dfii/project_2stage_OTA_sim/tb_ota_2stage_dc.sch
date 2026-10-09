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
C {vsource.sym} 940 -660 0 0 {name=Vin_P value=0.6 savecurrent=false}
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

op

* ============================================================
* Important DC nodes
* ============================================================

print v(Vout)
print v(x1.out_s1)
print v(x1.vdiode_n)
print v(x1.VCM)
print v(ibias_500nA)

let verr = v(Vin_P)-v(Vout)

print v(Vin_P)
print v(Vout)
print verr

* ============================================================
* PTAIL_0
* ============================================================

let id_pt0    = abs(@m.x1.xptail_0.msky130_fd_pr__pfet_01v8[id])
let gm_pt0    = abs(@m.x1.xptail_0.msky130_fd_pr__pfet_01v8[gm])
let gds_pt0   = abs(@m.x1.xptail_0.msky130_fd_pr__pfet_01v8[gds])
let gmid_pt0  = gm_pt0/id_pt0
let gain_pt0  = gm_pt0/gds_pt0
let vth_pt0   = abs(@m.x1.xptail_0.msky130_fd_pr__pfet_01v8[vth])
let vdsat_pt0 = abs(@m.x1.xptail_0.msky130_fd_pr__pfet_01v8[vdsat])

print id_pt0 gm_pt0 gds_pt0 gmid_pt0 gain_pt0 vth_pt0 vdsat_pt0


* ============================================================
* PTAIL_1
* ============================================================

let id_pt1    = abs(@m.x1.xptail_1.msky130_fd_pr__pfet_01v8[id])
let gm_pt1    = abs(@m.x1.xptail_1.msky130_fd_pr__pfet_01v8[gm])
let gds_pt1   = abs(@m.x1.xptail_1.msky130_fd_pr__pfet_01v8[gds])
let gmid_pt1  = gm_pt1/id_pt1
let gain_pt1  = gm_pt1/gds_pt1
let vdsat_pt1 = abs(@m.x1.xptail_1.msky130_fd_pr__pfet_01v8[vdsat])

print id_pt1 gm_pt1 gds_pt1 gmid_pt1 gain_pt1 vdsat_pt1


* ============================================================
* PDIFF_N
* ============================================================

let id_pdn    = abs(@m.x1.xpdiff_n.msky130_fd_pr__pfet_01v8[id])
let gm_pdn    = abs(@m.x1.xpdiff_n.msky130_fd_pr__pfet_01v8[gm])
let gds_pdn   = abs(@m.x1.xpdiff_n.msky130_fd_pr__pfet_01v8[gds])
let gmid_pdn  = gm_pdn/id_pdn
let gain_pdn  = gm_pdn/gds_pdn
let vdsat_pdn = abs(@m.x1.xpdiff_n.msky130_fd_pr__pfet_01v8[vdsat])

print id_pdn gm_pdn gds_pdn gmid_pdn gain_pdn vdsat_pdn


* ============================================================
* PDIFF_P
* ============================================================

let id_pdp    = abs(@m.x1.xpdiff_p.msky130_fd_pr__pfet_01v8[id])
let gm_pdp    = abs(@m.x1.xpdiff_p.msky130_fd_pr__pfet_01v8[gm])
let gds_pdp   = abs(@m.x1.xpdiff_p.msky130_fd_pr__pfet_01v8[gds])
let gmid_pdp  = gm_pdp/id_pdp
let gain_pdp  = gm_pdp/gds_pdp
let vdsat_pdp = abs(@m.x1.xpdiff_p.msky130_fd_pr__pfet_01v8[vdsat])

print id_pdp gm_pdp gds_pdp gmid_pdp gain_pdp vdsat_pdp


* ============================================================
* NLOAD_0
* ============================================================

let id_n0    = abs(@m.x1.xnload_0.msky130_fd_pr__nfet_01v8[id])
let gm_n0    = abs(@m.x1.xnload_0.msky130_fd_pr__nfet_01v8[gm])
let gds_n0   = abs(@m.x1.xnload_0.msky130_fd_pr__nfet_01v8[gds])
let gmid_n0  = gm_n0/id_n0
let gain_n0  = gm_n0/gds_n0
let vdsat_n0 = abs(@m.x1.xnload_0.msky130_fd_pr__nfet_01v8[vdsat])

print id_n0 gm_n0 gds_n0 gmid_n0 gain_n0 vdsat_n0


* ============================================================
* NLOAD_1
* ============================================================

let id_n1    = abs(@m.x1.xnload_1.msky130_fd_pr__nfet_01v8[id])
let gm_n1    = abs(@m.x1.xnload_1.msky130_fd_pr__nfet_01v8[gm])
let gds_n1   = abs(@m.x1.xnload_1.msky130_fd_pr__nfet_01v8[gds])
let gmid_n1  = gm_n1/id_n1
let gain_n1  = gm_n1/gds_n1
let vdsat_n1 = abs(@m.x1.xnload_1.msky130_fd_pr__nfet_01v8[vdsat])

print id_n1 gm_n1 gds_n1 gmid_n1 gain_n1 vdsat_n1


* ============================================================
* PTAIL_2
* ============================================================

let id_pt2    = abs(@m.x1.xptail_2.msky130_fd_pr__pfet_01v8[id])
let gm_pt2    = abs(@m.x1.xptail_2.msky130_fd_pr__pfet_01v8[gm])
let gds_pt2   = abs(@m.x1.xptail_2.msky130_fd_pr__pfet_01v8[gds])
let gmid_pt2  = gm_pt2/id_pt2
let gain_pt2  = gm_pt2/gds_pt2
let vdsat_pt2 = abs(@m.x1.xptail_2.msky130_fd_pr__pfet_01v8[vdsat])

print id_pt2 gm_pt2 gds_pt2 gmid_pt2 gain_pt2 vdsat_pt2


* ============================================================
* NLOAD_2
* ============================================================

let id_n2    = abs(@m.x1.xnload_2.msky130_fd_pr__nfet_01v8[id])
let gm_n2    = abs(@m.x1.xnload_2.msky130_fd_pr__nfet_01v8[gm])
let gds_n2   = abs(@m.x1.xnload_2.msky130_fd_pr__nfet_01v8[gds])
let gmid_n2  = gm_n2/id_n2
let gain_n2  = gm_n2/gds_n2
let vdsat_n2 = abs(@m.x1.xnload_2.msky130_fd_pr__nfet_01v8[vdsat])

print id_n2 gm_n2 gds_n2 gmid_n2 gain_n2 vdsat_n2

.endc

"}
