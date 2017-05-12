#encoding: utf-8

import sys

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

def pline(srcl, rts):
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

def handle(srcf,rsf,rtf):
	rts=ldrtf(rtf)
	with open(rsf,"w") as fwrt:
		with open(srcf) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=pline(tmp.decode("utf-8").split(" "),rts)
					fwrt.write(tmp.encode("utf-8"))
					fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),sys.argv[3].decode("utf-8"))
