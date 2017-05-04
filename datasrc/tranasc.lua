require "hdf5"

function ldvec(fsrc,vsize)
	local file=io.open(fsrc)
	local num=file:read("*n")
	local rs={}
	while num do
		table.insert(rs,num)
		num=file:read("*n")
	end
	file:close()
	ts=torch.FloatTensor(rs)
	return ts:reshape(#rs/vsize,vsize)
end

ti=hdf5.open("duse/traini.hdf5","r")
tt=hdf5.open("duse/traint.hdf5","r")
di=hdf5.open("duse/devi.hdf5","r")
dt=hdf5.open("duse/devt.hdf5","r")

ntrain=4596
ndev=309

traind={}
devd={}

for i=ntrain,1,-1 do
	local curid=tostring(i)
	table.insert(traind,{ti:read(curid):all(),tt:read(curid):all()})
end
ti:close()
tt:close()
for i=ndev,1,-1 do
	local curid=tostring(i)
	table.insert(devd,{di:read(curid):all(),dt:read(curid):all()})
end
di:close()
dt:close()
torch.save("data.asc",{traind,devd,ldvec("duse/100wvec.txt",100)})
