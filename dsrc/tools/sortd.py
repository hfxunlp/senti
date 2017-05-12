#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def sortf(fsrc,frs,freqf):
	l=[]
	storage={}
	with open(fsrc) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				fcache=tmp.split(" ")
				use=[]
				for fu in fcache:
					tmp=fu.strip()
					if tmp:
						use.append(tmp)
				lgth=len(use)
				tmp=" ".join(use)
				if lgth!=1:
					if lgth in storage:
						storage[lgth].append(tmp)
					else:
						l.append(lgth)
						storage[lgth]=[tmp]
	l.sort(reverse=True)
	with open(frs,"w") as fwrtd:
		with open(freqf,"w") as fwrtf:
			for lu in l:
				cwrtl=storage[lu]
				tmp="\n".join(cwrtl)+"\n"
				fwrtd.write(tmp.encode("utf-8"))
				tmp=str(lu)+"	"+str(len(cwrtl))+"\n"
				fwrtf.write(tmp.encode("utf-8"))

if __name__=="__main__":
	sortf(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),sys.argv[3].decode("utf-8"))
