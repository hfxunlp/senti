#encoding: utf-8

#请 输入
#这 句 话
#那 句 话
#{u'\u8fd9 \u53e5 \u8bdd': [[52, 17, 185], [240, 14, 0], [227, 27, 0], [0, 0, 256]], u'\u8bf7 \u8f93\u5165': [[188, 36, 30], [220, 35, 0], [0, 0, 255]], u'\u90a3 \u53e5 \u8bdd': [[147, 44, 64], [240, 14, 0], [228, 26, 0], [0, 0, 256]]}
#[[u'\u8bf7', u'\u8f93\u5165'], [''], [u'\u8fd9', u'\u53e5', u'\u8bdd'], [''], [u'\u90a3', u'\u53e5', u'\u8bdd'], ['']]
#[[[188, 36, 30], [220, 35, 0]], [[0, 0, 255]], [[52, 17, 185], [240, 14, 0], [227, 27, 0]], [[0, 0, 255]], [[147, 44, 64], [240, 14, 0], [228, 26, 0]], [[0, 0, 255]]]
#[[0, 0, 255], [0, 0, 255], [0, 0, 256], [0, 0, 255], [0, 0, 256], [0, 0, 255]]


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def nobigger(inum, lim):
	if inum>lim:
		return lim
	else:
		return inum

def expandColor(clin):
	tmp=clin*int(1.2)
	if tmp>255:
		return 255
	else:
		return tmp

def render_word(word, wcolor, gbase,addpos,addneg,addnone):
	pos, neg, none = [nobigger(cu,255) for cu in wcolor]
	pos+=addpos
	neg+=addneg
	if none>pos and none>neg:
		return "".join(["<font size=\"5\">",word,"</font>"])
	else:
		if pos>neg:
			curcolor=str(pos)
			#curcolor="255"
			return "".join(["<font size=\"5\" style=\"color:rgb(",str(expandColor(neg)),",",curcolor,",0)\">",word,"</font>"])
		else:
			curcolor=str(expandColor(neg))
			#curcolor="255"
			return "".join(["<font size=\"5\" style=\"color:rgb(",curcolor,",0,0)\">",word,"</font>"])

def render(iseq, pseq, sentp):
	gbase = str(0)
	rs=[]
	for sequ, coloru, sentu in zip(iseq, pseq, sentp):
		tmp=sequ[0].strip()
		if tmp:
			addpos,addneg,addnone=sentu
			cache=[]
			for word, wcolor in zip(sequ, coloru):
				cache.append(render_word(word, wcolor, gbase,addpos,addneg,addnone))
			rs.append(" ".join(cache))
	return "<br />".join(rs)
