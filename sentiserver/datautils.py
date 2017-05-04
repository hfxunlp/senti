#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

splitcode=set([u"。", u"？", u"！", u"；"])
puncds=set(["/wt","/wj","/ww","/wf","/wd"])

def _cutParagraph(strin):
	global splitcode
	rs=[]
	ind=0
	lind=0
	for stru in strin:
		if stru in splitcode:
			rs.append(strin[lind:ind+1])
			ind+=1
			lind=ind
		else:
			ind+=1
	if lind<ind:
		rs.append(strin[lind:])
	return rs

def fixseg(lin):
	global puncds
	rs=[]
	for lu in lin:
		if lu[:3] in puncds:
			tmp=lu[4:].strip()
		else:
			tmp=lu.strip()
		if tmp:
			rs.append(tmp)
	return rs

def cutParagraph(strin):
	if strin.find("\r")>0:
		splsgn="\r"
	else:
		splsgn="\n"
	tmp=strin.split(splsgn)
	rs=[]
	for tmpu in tmp:
		tt=tmpu.strip()
		if tt:
			tmp=fixseg(_cutParagraph(tt))
			if tmp:
				rs.extend(tmp)
				rs.append("\n")
	return rs

def ldrtf(fname):
	rs=set()
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				if not tmp in rs:
					rs.add(tmp)
	return rs

def reduceline(srcl):
	global rts
	rs=[]
	for srcu in srcl:
		ind=srcu.rfind("/")
		wd=srcu[:ind]
		tag=srcu[ind+1:]
		if tag in rts:
			rs.append(tag)
		else:
			rs.append(wd)
	return " ".join(rs)

def sort(srcl):
	l=[]
	storage={}
	for line in srcl:
		lgth=len(line.split(" "))
		if lgth in storage:
			storage[lgth].append(line)
		else:
			l.append(lgth)
			storage[lgth]=[line]
	l.sort(reverse=True)
	rs=[]
	for lu in l:
		rs.extend(storage[lu])
	return rs

def reducebytag(ls):
	rs={}
	for lu in ls:
		rs[lu]=reduceline(lu.split(" "))
	return rs

def filterChaoes(srcl):
	rs=set()
	for srcu in srcl:
		tmp=srcu.strip()
		if tmp and not tmp in rs:
			rs.add(tmp)
	return rs

def restore(transl):
	rs=[]
	for tranu in transl:
		tmp=tranu[0]
		if type(tmp)==dict:
			tmp=tmp.get("tgt","")
			if tmp:
				rs.append(tmp)
	return " ".join(rs)

def makeBatches(lin,splt):
	rs=[]
	start=0
	for splu in splt:
		end=start+splu
		rs.append(lin[start:end])
		start=end
	return rs

def padmat(l2,padv):
	if len(l2)==1:
		return l2
	else:
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

def mapBatch(batch, mapd, unkid, padv, eosid):
	rs=[]
	for bu in batch:
		cache=[mapd.get(wd, unkid) for wd in bu.split(" ")]
		cache.append(eosid)
		rs.append(cache)
	return padmat(rs, padv)

def mergeBatches(batches):
	rs=[]
	for batch in batches:
		rs.extend(batch)
	return rs

def buildMap(l1,l2):
	rs={}
	for lu1, lu2 in zip(l1, l2):
		rs[lu1]=lu2
	return rs

def getISeq(strin):
	tmp=strin.split(" ")
	rs=[]
	for tmpu in tmp:
		ind=tmpu.rfind("/")
		if ind>0:
			rs.append(tmpu[:ind])
		else:
			rs.append(tmpu)
	return rs

def formatPred(seqs, tagm, rsm):
	rsi=[]
	rsp=[]
	sentp=[]
	for sequ in seqs:
		tmp=sequ.strip()
		if tmp:
			if sequ in tagm:
				rtd=tagm[sequ]
				if rtd in rsm:
					iSeq=getISeq(tmp)
					rsi.append(iSeq)
					p=rsm[rtd]
					rsp.append(p[:len(iSeq)])
					sentp.append(p[-1])
				else:
					iSeq=getISeq(tmp)
					rsi.append(tmp)
					rsp.append([[0,0,255] for i in xrange(len(iSeq))])
					sentp.append([0,0,255])					
			else:
				iSeq=getISeq(tmp)
				rsi.append(tmp)
				rsp.append([[0,0,255] for i in xrange(len(iSeq))])
				sentp.append([0,0,255])
		else:
			iSeq=getISeq(tmp)
			if iSeq:
				rsi.append(iSeq)
				rsp.append([[0,0,255] for i in xrange(len(iSeq))])
				sentp.append([0,0,255])
	return rsi, rsp, sentp

def mapBatches(batches):
	global mapd, unkid, padv, eosid
	rs=[]
	for batch in batches:
		rs.append(map(list, zip(*mapBatch(batch, mapd, unkid, padv, eosid))))
	return rs

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

def poweron():
	global rts,mapd,unkid,eosid,padv
	rts=ldrtf("ref/reptag.txt")
	mapd=ldmap("ref/words.map")
	unkid=mapd["<unk>"]
	eosid=mapd["<eos>"]
	padv=mapd["<pad>"]
