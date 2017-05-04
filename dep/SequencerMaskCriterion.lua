local SequencerMaskCriterion, parent = torch.class('nn.SequencerMaskCriterion', 'nn.Criterion')

function SequencerMaskCriterion:__init(criterion, maskid)
	parent.__init(self)
	self.criterion = criterion
	self.maskid = maskid
end

function SequencerMaskCriterion:updateOutput(input, target)

	local isize = input:size()
	local seqlen = isize[1]
	local bsize = isize[2]
	local osize = isize[3]
	local nbsize = seqlen * bsize
	self.input = input:clone():reshape(nbsize, osize)
	self.target = target:reshape(nbsize)
	self._mask = self.target:eq(self.maskid)
	self._mask = self._mask:reshape(nbsize, 1):expandAs(self.input)
	self.input:maskedFill(self._mask, 0)
	self.output = self.criterion:updateOutput(self.input, self.target)
	return self.output

end

function SequencerMaskCriterion:updateGradInput(input, target)
	self.gradInput = self.criterion:updateGradInput(self.input, self.target)
	self.gradInput:maskedFill(self._mask, 0)
	self.gradInput = self.gradInput:reshape(input:size())
	return self.gradInput
end
