require "nn"
require "dpnn"
require "dep.vecLookupZero"
require "dep.SequencerMaskCriterion"
require "dep.SeqDropout"
require "cunn"
require "cudnn"

function getnn()
	--return getonn()
	return getnnn()
end

function getonn()
	wvec = nil
	--local lmod = loadObject("modrs/nnmod.asc").module
	local lmod = torch.load("modrs/nnmod.asc").module
	return lmod
end

function getnnn()

	--require "models.baseline"
	require "models.bgru"
	--require "models.sentencebaseline"
	return getusenn(4)

end

function getcrit()
	return nn.SequencerMaskCriterion(nn.ClassNLLCriterion(),1);
end

--[[function getcrit()
	--require "dep.MaskCriterion"
	return nn.ClassNLLCriterion();
	--return nn.MaskCriterion(nn.ClassNLLCriterion(),1);
end]]
