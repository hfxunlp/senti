function loadmodel(fname)
	local nnmod = torch.load(fname).modules[1]:clone()
	nnmod:remove(4)--remove the nn.Select
	local lm = nn.Bottle(nnmod:get(-2))
	nnmod:remove()
	nnmod:remove()
	nnmod:add(lm)
	nnmod:add(nn.Narrow(3, 2, 3))
	nnmod:add(nn.Bottle(nn.SoftMax()))
	nnmod:evaluate()
	nnmod:cuda()
	return nnmod
end
