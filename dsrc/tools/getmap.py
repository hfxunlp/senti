#encoding: utf-8

import sys

def handle(srcf,rsf,kfreq):
	fd={}
	with open(srcf) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8").split(" ")
				for tmpu in tmp:
					fd[tmpu]=fd.get(tmpu,0)+1
	tmp=["<unk>","<eos>"]
	for k, v in fd.iteritems():
		if v>kfreq:
			k=k.strip()
			if k:
				tmp.append(k)
	tmp.append("<pad>")
	print("get:"+str(len(tmp))+" words")
	with open(rsf,"w") as fwrt:
		tmp="\n".join(tmp)
		fwrt.write(tmp.encode("utf-8"))

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"),int(sys.argv[3].decode("utf-8")))
