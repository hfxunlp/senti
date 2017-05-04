local MaskCriterion, parent = torch.class('nn.MaskCriterion', 'nn.Criterion')

function MaskCriterion:__init(criterion, maskid)
	parent.__init(self)
	self.criterion = criterion
	self.maskid = maskid
end

function MaskCriterion:updateOutput(input, target)

	local bsize = input:size(1)
	self._mask = target:eq(self.maskid):reshape(bsize, 1):expandAs(input)
	self.input = input:clone():maskedFill(self._mask, 0)
	self.output = self.criterion:updateOutput(self.input, target)
	return self.output

end

function MaskCriterion:updateGradInput(input, target)
	self.gradInput = self.criterion:updateGradInput(self.input, target)
	self.gradInput:maskedFill(self._mask, 0)
	return self.gradInput
end
