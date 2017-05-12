#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from random import random

def ldmap(fname):
	rs={}
	curid=1
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				if not tmp in rs:
					rs[tmp]=curid
					curid+=1
	return rs

def exvec(mpf,vecf,rsf,vecsize):
	wdm=ldmap(mpf)
	rsd={}
	with open(vecf) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				ind=tmp.find(" ")
				wd=tmp[:ind]
				if wd=="<unk>":
					unkvec=tmp[ind+1:]
				if wd in wdm:
					rsd[wdm[wd]]=tmp[ind+1:]
	if "<pad>" in wdm:
		rsd[wdm["<pad>"]]=" ".join(["0" for i in xrange(vecsize)])
	if not unkvec:
		unkvec=" ".join([str(random()*2-1) for i in xrange(vecsize)])
	with open(rsf,"w") as fwrt:
		for i in xrange(1,len(wdm)+1):
			if i in rsd:
				tmp=rsd[i]
			else:
				tmp=unkvec
			fwrt.write(tmp.encode("utf-8"))
			fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	exvec(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),sys.argv[3].decode("utf-8"),int(sys.argv[4].decode("utf-8")))