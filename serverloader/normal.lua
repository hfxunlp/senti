function loadmodel(fname)
	local nnmod = torch.load(fname).modules[1]:clone()
	nnmod:remove()
	nnmod:add(nn.Narrow(3, 2, 3))
	nnmod:add(nn.Bottle(nn.SoftMax()))
	nnmod:evaluate()
	nnmod:cuda()
	return nnmod
end
