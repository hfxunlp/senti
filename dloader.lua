require "cutorch"

local function gpuvec(tbin)
	local rs={}
	for _, v in ipairs(tbin) do
		local _i, _t = unpack(v)
		rs[_]={_i:cudaLong(),_t:cudaLong()}
	end
	return rs
end

local _traind, _devd, _wvec = unpack(torch.load("datasrc/100data.asc"))

wvec=_wvec:float()

traind=gpuvec(_traind)
devd=gpuvec(_devd)

ntrain=#traind
ndev=#devd
nword=wvec:size(1)
