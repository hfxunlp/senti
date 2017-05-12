#encoding: utf-8

import sys
from random import sample

def ldsrc(fname):
	rs=[]
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				rs.append(tmp)
	return rs

def handle(srcf,rstf,rsvf):
	srcd=ldsrc(srcf)
	t=len(srcd)
	dinds=set(sample([i for i in xrange(1,t+1)],t/20))
	curid=1
	with open(rstf,"w") as fwrt:
		with open(rsvf,"w") as fwrd:
			for srcu in srcd:
				if curid in dinds:
					fwrd.write(srcu.encode("utf-8"))
					fwrd.write("\n".encode("utf-8"))
				else:
					fwrt.write(srcu.encode("utf-8"))
					fwrt.write("\n".encode("utf-8"))
				curid+=1

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),sys.argv[3].decode("utf-8"))
