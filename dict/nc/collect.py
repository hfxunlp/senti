#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os

def wrtset(fname,sw):
	tmp="\n".join(sw)
	with open(fname,"w") as fwrt:
		fwrt.write(tmp.encode("utf-8"))

ps=set()
ns=set()

for root, dirs, files in os.walk("src"):
	for file in files:
		if file.find("pos")!=-1:
			ispos=True
		else:
			if file.find("neg")==-1:
				print file
			ispos=False
		with open(os.path.join(root,file)) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					if ispos:
						if not tmp in ps:
							ps.add(tmp)
					else:
						if not tmp in ns:
							ns.add(tmp)

wrtset("pos.txt",ps)
wrtset("neg.txt",ns)