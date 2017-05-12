#encoding: utf-8

import sys

#读取源文件长度信息
def ldsrc(fname,maxlen,minlen=0):
	rsd={}
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=len(tmp.decode("utf-8").split(" "))
				if tmp<maxlen and tmp>minlen:
					rsd[tmp]=rsd.get(tmp,0)+1
	return rsd

#根据长度信息，切分数据
#sld:长度信息词典
#maxbatch:最大批量大小
#maxind:最大词索引数量
#maxpad:能容忍的最大填充位数
def splitter(sld,maxbatch,maxind,maxpad):
	rs=[]
	linfo=sld.keys()
	linfo.sort(reverse=True)
	cache=0#前一个长度的数据剩余的数量
	mlen=linfo[0]#当前cache的最大长度
	for lu in linfo:#对于每一个长度的序列
		#确定实际可用的最大批量值maxbatch_ground
		curl_maxbatch_ground=max(min(maxind/lu,maxbatch),1)#当前长度对应的最大批量
		if cache>0:#如果存在cache
			maxbatch_ground=max(min(maxind/mlen,maxbatch),1)
		else:
			maxbatch_ground=curl_maxbatch_ground
		ncontent=sld[lu]#获取当前长度序列的数量
		if ncontent>maxbatch_ground:#如果当前长度大于容许的最大批量大小
			if cache>0:#如果存在待缓存的剩余内容
				if mlen>lu+maxpad:#如果需要填充的位数大于能容忍的长度
					rs.append(cache)
				else:#如果当前序列的长度可以和前一批剩余的缓存合并
					maxcanmerge=ncontent%curl_maxbatch_ground#当前序列长度可以并入上一长度的数量
					maxmerge=maxcanmerge+cache#向cache并入maxcanmerge后，cache的大小
					if maxmerge>maxbatch_ground:#如果cache会大于能容忍的最大batch
						tmp=maxmerge/maxbatch_ground
						rs.extend([maxbatch_ground for i in xrange(tmp)])
						ncontent-=tmp*maxbatch_ground-cache#更新当前长度剩余的序列数量
					else:
						rs.append(maxmerge)
						ncontent-=maxcanmerge
				if ncontent>0:#如果处理cache后还有剩余
					rs.extend([curl_maxbatch_ground for i in xrange(ncontent/curl_maxbatch_ground)])#继续压入
					cache=ncontent%curl_maxbatch_ground#更新cache
					if cache>0:#如果当前长度序列被压入cache
						mlen=lu
				else:
					cache=0
			else:#如果不存在待缓存的剩余内容
				rs.extend([maxbatch_ground for i in xrange(ncontent/maxbatch_ground)])
				cache=ncontent%maxbatch_ground#更新cache，将当前长度剩余的序列压入cache
				if cache>0:
					mlen=lu#同时更新序列的最大批量长度信息
		else:#如果当前长度不大于容许的最大批量大小
			if cache>0:#如果存在cache
				if cache+ncontent>maxbatch_ground:
					rs.append(cache)
					rs.append(ncontent)
					cache=0
				else:
					if lu+maxpad>mlen:
						cache+=ncontent
					else:
						rs.append(cache)
						cache=ncontent
						mlen=lu
			else:
				cache=ncontent
				mlen=lu
	if cache>0:
		rs.append(cache)
	print "Process:",sumlist(rs),"lines, split to:",len(rs),"batches"
	return rs

def sumlist(lin):
	rs=0
	for lu in lin:
		rs+=lu
	return rs

def wrtrs(rsl,fname):
	tmp="\n".join([str(i) for i in rsl])
	with open(fname,"w") as fwrt:
		fwrt.write(tmp.encode("utf-8"))

#src:源文件，按长度降序排列
#rs:切分配置文件
def handle(src,rs):
	maxbatch=32#最大批量大小
	maxind=maxbatch*200#最大词索引数量
	maxpad=0#maxbatch/8#最大填充长度
	wrtrs(splitter(ldsrc(src,100000),maxbatch,maxind,maxpad),rs)

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
