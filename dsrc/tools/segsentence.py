#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#punc=set([u"！",u"。",u"？",u"；",u"，"])
punc=set([u"！",u"。",u"？",u"；",u"."])
apunc=set([u"”"])

def segline(strin):
	global punc,apunc
	start=0
	end=0
	rs=[]
	apr=False
	for stru in strin:
		if stru in punc:
			apr=True
		else:
			if apr:
				if stru in apunc:
					rs.append(strin[start:end+1].strip())
					start=end+1
				else:
					rs.append(strin[start:end].strip())
					start=end
				apr=False
		end+=1
	if apr or end!=start:
		rs.append(strin[start:].strip())
	return "\n".join(rs)

def segf(srcf,rsf):
	with open(rsf,"w") as fwrt:
		with open(srcf) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					tmp=segline(tmp)
					fwrt.write(tmp.encode("utf-8"))
					fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	segf(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
