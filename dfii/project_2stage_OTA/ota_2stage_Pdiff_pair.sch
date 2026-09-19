v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 810 -140 810 -80 {lab=0}
N 260 -80 700 -80 {lab=0}
N 260 -140 260 -80 {lab=0}
N 300 -170 400 -170 {lab=vdiode_n}
N 260 -280 260 -200 {lab=vdiode_n}
N 260 -320 260 -280 {lab=vdiode_n}
N 260 -230 330 -230 {lab=vdiode_n}
N 330 -230 330 -170 {lab=vdiode_n}
N 560 -170 660 -170 {lab=out_s1}
N 560 -230 560 -170 {lab=out_s1}
N 440 -140 440 -80 {lab=0}
N 440 -170 450 -170 {lab=0}
N 450 -170 450 -80 {lab=0}
N 250 -170 260 -170 {lab=0}
N 250 -170 250 -80 {lab=0}
N 250 -80 260 -80 {lab=0}
N 810 -170 820 -170 {lab=0}
N 820 -170 820 -80 {lab=0}
N 810 -80 820 -80 {lab=0}
N 440 -320 440 -200 {lab=out_s1}
N 810 -320 810 -200 {lab=Vout}
N 260 -350 440 -350 {lab=VCM}
N 350 -420 350 -350 {lab=VCM}
N 260 -420 260 -380 {lab=VCM}
N 260 -420 350 -420 {lab=VCM}
N 350 -420 440 -420 {lab=VCM}
N 440 -420 440 -380 {lab=VCM}
N 480 -350 520 -350 {lab=vmp}
N 180 -350 220 -350 {lab=vmm}
N 560 -260 560 -230 {lab=out_s1}
N 440 -260 560 -260 {lab=out_s1}
N 700 -80 820 -80 {lab=0}
N 660 -170 770 -170 {lab=out_s1}
N 560 -260 610 -260 {lab=out_s1}
N 780 -260 810 -260 {lab=Vout}
N 770 -260 780 -260 {lab=Vout}
N 670 -260 710 -260 {lab=#net1}
N 740 -240 740 -80 {lab=0}
N 350 -500 350 -420 {lab=VCM}
N 810 -500 810 -320 {lab=Vout}
N 120 -530 310 -530 {lab=vbias_p}
N 350 -530 360 -530 {lab=VDD}
N 360 -600 360 -530 {lab=VDD}
N 80 -600 80 -560 {lab=VDD}
N 80 -600 360 -600 {lab=VDD}
N 70 -530 80 -530 {lab=VDD}
N 70 -600 70 -530 {lab=VDD}
N 70 -600 90 -600 {lab=VDD}
N 810 -530 820 -530 {lab=VDD}
N 820 -600 820 -530 {lab=VDD}
N 810 -600 810 -560 {lab=VDD}
N 350 -600 820 -600 {lab=VDD}
N 350 -600 350 -560 {lab=VDD}
N 80 -500 80 -440 {lab=vbias_p}
N 80 -480 140 -480 {lab=vbias_p}
N 140 -530 140 -480 {lab=vbias_p}
N 140 -480 660 -480 {lab=vbias_p}
N 660 -530 770 -530 {lab=vbias_p}
N 660 -530 660 -480 {lab=vbias_p}
N 810 -350 960 -350 {lab=Vout}
N 960 -290 960 -80 {lab=0}
N 820 -80 960 -80 {lab=0}
C {sky130_fd_pr/nfet_01v8.sym} 280 -170 0 1 {name=NLOAD_0
W=1
L=1
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
C {sky130_fd_pr/nfet_01v8.sym} 420 -170 0 0 {name=NLOAD_1
W=1
L=1
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
C {sky130_fd_pr/nfet_01v8.sym} 790 -170 0 0 {name=NLOAD_2
W=1
L=1
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
C {sky130_fd_pr/pfet_01v8.sym} 240 -350 0 0 {name=PDIFF_N
W=1
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
C {sky130_fd_pr/pfet_01v8.sym} 460 -350 0 1 {name=PDIFF_P
W=1
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
C {lab_wire.sym} 340 -420 0 0 {name=p1 sig_type=std_logic lab=VCM}
C {lab_wire.sym} 330 -230 0 0 {name=p3 sig_type=std_logic lab=vdiode_n}
C {sky130_fd_pr/pfet_01v8.sym} 330 -530 0 0 {name=PTAIL_1
W=1
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
C {sky130_fd_pr/pfet_01v8.sym} 790 -530 0 0 {name=PTAIL_2
W=1
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
C {sky130_fd_pr/pfet_01v8.sym} 100 -530 0 1 {name=PTAIL_0
W=1
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
C {isource.sym} 80 -410 0 0 {name=I0 value=\{IBIAS\}}
C {gnd.sym} 80 -380 0 0 {name=l1 lab=0}
C {gnd.sym} 250 -80 0 0 {name=l2 lab=0}
C {lab_wire.sym} 900 -350 0 0 {name=p4 sig_type=std_logic lab=Vout}
C {lab_wire.sym} 530 -260 0 0 {name=p5 sig_type=std_logic lab=out_s1}
C {lab_wire.sym} 510 -480 0 0 {name=p6 sig_type=std_logic lab=vbias_p}
C {vdd.sym} 80 -600 0 0 {name=l3 lab=VDD}
C {lab_wire.sym} 520 -350 0 0 {name=p2 sig_type=std_logic lab=vmp}
C {lab_wire.sym} 200 -350 0 0 {name=p7 sig_type=std_logic lab=vmm}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 640 -260 3 0 {name=CMILLER model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/res_high_po.sym} 740 -260 3 0 {name=RMILLER
W=1
L=1
model=res_high_po
spiceprefix=X
mult=1}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 960 -320 0 0 {name=CL model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
