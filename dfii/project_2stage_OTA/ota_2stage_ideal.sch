v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 240 -100 240 -50 {lab=0}
N 240 -50 240 -40 {lab=0}
N 680 -100 680 -40 {lab=0}
N 580 -100 580 -40 {lab=0}
N 340 -100 340 -40 {lab=0}
N 540 -110 540 -40 {lab=0}
N 580 -200 580 -160 {lab=Vout}
N 680 -200 680 -160 {lab=Vout}
N 480 -150 540 -150 {lab=out_s1}
N 480 -200 480 -150 {lab=out_s1}
N 240 -200 240 -160 {lab=out_s1}
N 340 -200 340 -160 {lab=out_s1}
N 160 -110 200 -110 {lab=Vin_N}
N 140 -150 200 -150 {lab=Vin_P}
N 420 -280 500 -280 {lab=out_s1}
N 680 -280 680 -200 {lab=Vout}
N 240 -200 420 -200 {lab=out_s1}
N 420 -200 440 -200 {lab=out_s1}
N 440 -200 450 -200 {lab=out_s1}
N 450 -200 460 -200 {lab=out_s1}
N 460 -200 470 -200 {lab=out_s1}
N 470 -200 480 -200 {lab=out_s1}
N 420 -280 420 -200 {lab=out_s1}
N 240 -40 680 -40 {lab=0}
N 580 -200 680 -200 {lab=Vout}
N 140 -110 160 -110 {lab=Vin_N}
N 340 -360 680 -360 {lab=out_s1}
N 340 -360 340 -200 {lab=out_s1}
N 560 -280 590 -280 {lab=#net1}
N 650 -280 680 -280 {lab=Vout}
C {vccs.sym} 240 -130 0 0 {name=G_STAGE1 value=5u }
C {vccs.sym} 580 -130 0 0 {name=G_STAGE2 value=54.4u}
C {res.sym} 340 -130 0 0 {name=ROUT_S1
value=29.7Meg
footprint=1206
device=resistor
m=1}
C {res.sym} 680 -130 0 0 {name=ROUT_S2
value=2.81Meg
footprint=1206
device=resistor
m=1}
C {gnd.sym} 240 -40 0 0 {name=l1 lab=0}
C {lab_wire.sym} 190 -150 0 0 {name=p1 sig_type=std_logic lab=Vin_P}
C {lab_wire.sym} 190 -110 0 0 {name=p3 sig_type=std_logic lab=Vin_N}
C {lab_wire.sym} 400 -200 0 0 {name=p2 sig_type=std_logic lab=out_s1}
C {lab_wire.sym} 660 -200 0 0 {name=p4 sig_type=std_logic lab=Vout}
C {capa.sym} 530 -280 3 0 {name=CMILLER
m=1
value=0.8p
footprint=1206
device="ceramic capacitor"}
C {ipin.sym} 140 -150 0 0 {name=p5 lab=Vin_P}
C {ipin.sym} 140 -110 0 0 {name=p6 lab=Vin_N}
C {opin.sym} 680 -360 0 0 {name=p7 lab=out_s1}
C {opin.sym} 680 -200 0 0 {name=p8 lab=Vout}
C {res.sym} 620 -280 3 0 {name=RMILLER
value=110k
footprint=1206
device=resistor
m=1}
