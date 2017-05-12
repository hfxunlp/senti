#encoding: utf-8

import sys

def handle(srcp,rsf):
	with open(rsf,"w") as fwrt:
		for tag in ["pos","neg","none"]:
			wtag=tag+" "
			with open(srcp+tag+".txt") as frd:
				for line in frd:
					tmp=line.strip()
					if tmp:
						fwrt.write(wtag.encode("utf-8"))
						tmp=tmp.decode("utf-8")
						fwrt.write(tmp.encode("utf-8"))
						fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
