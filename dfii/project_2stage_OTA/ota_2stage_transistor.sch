v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {1                    :                   1                                     :                          6} 210 -690 0 0 0.4 0.4 {}
T {1            :             1                          :                       12} 390 -60 0 0 0.4 0.4 {}
N 950 -140 950 -80 {lab=GND}
N 400 -80 840 -80 {lab=GND}
N 400 -140 400 -80 {lab=GND}
N 440 -170 540 -170 {lab=vdiode_n}
N 400 -280 400 -200 {lab=vdiode_n}
N 400 -320 400 -280 {lab=vdiode_n}
N 400 -230 470 -230 {lab=vdiode_n}
N 470 -230 470 -170 {lab=vdiode_n}
N 700 -170 800 -170 {lab=out_s1}
N 700 -230 700 -170 {lab=out_s1}
N 580 -140 580 -80 {lab=GND}
N 580 -170 590 -170 {lab=GND}
N 590 -170 590 -80 {lab=GND}
N 390 -170 400 -170 {lab=GND}
N 390 -170 390 -80 {lab=GND}
N 390 -80 400 -80 {lab=GND}
N 950 -170 960 -170 {lab=GND}
N 960 -170 960 -80 {lab=GND}
N 950 -80 960 -80 {lab=GND}
N 580 -320 580 -200 {lab=out_s1}
N 950 -320 950 -200 {lab=Vout}
N 400 -350 580 -350 {lab=VCM}
N 400 -420 400 -380 {lab=VCM}
N 400 -420 490 -420 {lab=VCM}
N 490 -420 580 -420 {lab=VCM}
N 580 -420 580 -380 {lab=VCM}
N 620 -350 660 -350 {lab=Vin_P}
N 320 -350 360 -350 {lab=Vin_N}
N 700 -260 700 -230 {lab=out_s1}
N 580 -260 700 -260 {lab=out_s1}
N 840 -80 960 -80 {lab=GND}
N 800 -170 910 -170 {lab=out_s1}
N 700 -260 750 -260 {lab=out_s1}
N 920 -260 950 -260 {lab=Vout}
N 910 -260 920 -260 {lab=Vout}
N 810 -260 850 -260 {lab=#net1}
N 490 -500 490 -420 {lab=VCM}
N 950 -500 950 -320 {lab=Vout}
N 260 -530 450 -530 {lab=ibias_500nA}
N 490 -530 500 -530 {lab=VDD}
N 500 -600 500 -530 {lab=VDD}
N 220 -600 220 -560 {lab=VDD}
N 220 -600 500 -600 {lab=VDD}
N 210 -530 220 -530 {lab=VDD}
N 210 -600 210 -530 {lab=VDD}
N 210 -600 230 -600 {lab=VDD}
N 950 -530 960 -530 {lab=VDD}
N 960 -600 960 -530 {lab=VDD}
N 950 -600 950 -560 {lab=VDD}
N 490 -600 960 -600 {lab=VDD}
N 490 -600 490 -560 {lab=VDD}
N 220 -500 220 -440 {lab=ibias_500nA}
N 220 -480 280 -480 {lab=ibias_500nA}
N 280 -530 280 -480 {lab=ibias_500nA}
N 280 -480 800 -480 {lab=ibias_500nA}
N 800 -530 910 -530 {lab=ibias_500nA}
N 800 -530 800 -480 {lab=ibias_500nA}
N 950 -350 1020 -350 {lab=Vout}
N 490 -420 490 -360 {lab=VCM}
N 490 -360 490 -350 {lab=VCM}
N 880 -240 880 -80 {lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 420 -170 0 1 {name=NLOAD_0
W=3.6
L=12
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 560 -170 0 0 {name=NLOAD_1
W=3.6
L=12
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 930 -170 0 0 {name=NLOAD_2
W=3.6
L=2
nf=1 
mult=2
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 380 -350 0 0 {name=PDIFF_N
W=7.4
L=1
body=VDD
nf=1
mult=12
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 600 -350 0 1 {name=PDIFF_P
W=7.4
L=1
body=VDD
nf=1
mult=12
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_wire.sym} 480 -420 0 0 {name=p1 sig_type=std_logic lab=VCM}
C {lab_wire.sym} 470 -230 0 0 {name=p3 sig_type=std_logic lab=vdiode_n}
C {sky130_fd_pr/pfet_01v8.sym} 470 -530 0 0 {name=PTAIL_1
W=1.76
L=1
body=VDD
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 930 -530 0 0 {name=PTAIL_2
W=1.76
L=1
body=VDD
nf=1
mult=6
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 240 -530 0 1 {name=PTAIL_0
W=1.76
L=1
body=VDD
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_wire.sym} 1010 -350 0 0 {name=p4 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 670 -260 0 0 {name=p5 sig_type=std_logic lab=out_s1}
C {vdd.sym} 220 -600 0 0 {name=l3 lab=VDD}
C {iopin.sym} 210 -600 2 0 {name=p8 lab=VDD}
C {iopin.sym} 390 -80 2 0 {name=p9 lab=GND}
C {ipin.sym} 220 -440 0 0 {name=p10 lab=ibias_500nA}
C {ipin.sym} 320 -350 0 0 {name=p2 lab=Vin_N}
C {ipin.sym} 660 -350 2 0 {name=p7 lab=Vin_P}
C {opin.sym} 1020 -350 0 0 {name=p12 lab=Vout}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 780 -260 3 0 {name=CMILLER model=cap_mim_m3_1 W=19 L=19 MF=1 spiceprefix=X}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po_0p35.sym} 880 -260 3 0 {name=RMILLER
L=31.5
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
