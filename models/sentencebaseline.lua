function getusenn(nclass,pdrop1，pdrop2)
	local dr=pdrop1 or 0.2
	local cdr=pdrop2 or 0.2
	local isize=wvec:size(2)
	local hsize=math.ceil(isize/2)
	--local hsize=isize
	return nn.Sequential()
		:add(nn.vecLookup(wvec))
		:add(nn.SeqDropout(dr))
		:add(cudnn.GRU(isize,hsize,1))
		:add(nn.Select(1, -1))
		--:add(nn.Dropout(cdr))
		:add(nn.Linear(hsize,nclass))
		:add(nn.LogSoftMax())
end
