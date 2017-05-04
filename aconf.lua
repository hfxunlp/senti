starterate=math.huge--warning:only used as init erate, not asigned to criterion

runid="170420_0.2_0.2_1_h50_bgrulsoftp_randcrit"
logd="logs"

ieps=1
warmcycle=4
expdecaycycle=4
gtraincycle=32

modlr=1/8192--1024

earlystop=gtraincycle*2

csave=3

lrdecaycycle=4

recyclemem=0.05
