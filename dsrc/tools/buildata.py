#encoding: utf-8

import sys
import h5py,numpy

from random import shuffle

def padmat(l2,padv):
	slen=0
	rs=[]
	for lu in l2:
		tmp=len(lu)
		if tmp>slen:
			slen=tmp
	for lu in l2:
		tmp=slen-len(lu)
		if tmp>0:
			tmpl=[padv for i in xrange(tmp)]
			tmpl.extend(lu)
			rs.append(tmpl)
			#lu.extend([padv for i in xrange(tmp)])
		else:
			rs.append(lu)
	return rs

def shufflepair(srcm1, srcm2):
	bsize=srcm1.shape[0]
	if bsize == 1:
		return srcm1, srcm2
	else:
		rind = [i for i in xrange(bsize)]
		shuffle(rind)
		rsm1 = numpy.zeros(srcm1.shape, dtype=srcm1.dtype)
		rsm2 = numpy.zeros(srcm2.shape, dtype=srcm2.dtype)
		curid = 0
		for ru in rind:
			rsm1[curid] = srcm1[ru]
			rsm2[curid] = srcm2[ru]
			curid+=1
		return rsm1, rsm2

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

def ldset(fname):
	rs=set()
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				if not tmp in rs:
					rs.add(tmp)
	return rs

def mapline(ld,mapd,unkid,eosid,pdict,ndict):
	pmap={"unk":1,"pos":2,"neg":3,"none":4}
	id=[]
	td=[]
	stag=pmap.get(ld[0],1)
	for lu in ld[1:]:
		id.append(mapd.get(lu,unkid))
		if lu in pdict:
			td.append(2)
		elif lu in ndict:
			td.append(3)
		else:
			td.append(1)
	id.append(eosid)
	td.append(stag)
	return id, td

def handle(srcf,rsif,rstf,splf,mapf,pdictf,ndictf):
	rsif=h5py.File(rsif,"w")
	rstf=h5py.File(rstf,"w")
	curid=1
	mapd=ldmap(mapf)
	pdict=ldset(pdictf)
	ndict=ldset(ndictf)
	unkid=mapd["<unk>"]
	eid=mapd["<eos>"]
	padv=mapd["<pad>"]
	with open(srcf) as frd:
		with open(splf) as spl:
			for line in spl:
				tmp=line.strip()
				if tmp:
					tmp=int(tmp.decode("utf-8"))
					tid=[]
					ttd=[]
					for i in xrange(tmp):
						lini,lint=mapline(frd.readline().strip().decode("utf-8").split(" "),mapd,unkid,eid,pdict,ndict)
						tid.append(lini)
						ttd.append(lint)
					tid=numpy.array(padmat(tid,padv),dtype=numpy.int32)
					ttd=numpy.array(padmat(ttd,1),dtype=numpy.int32)
					tid, ttd=shufflepair(tid,ttd)
					wrtkey=str(curid)
					rsif[wrtkey]=tid.T
					rstf[wrtkey]=ttd.T
					curid+=1
	rsif.close()
	rstf.close()

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),sys.argv[3].decode("utf-8"),sys.argv[4].decode("utf-8"),sys.argv[5].decode("utf-8"),sys.argv[6].decode("utf-8"),sys.argv[7].decode("utf-8"))
