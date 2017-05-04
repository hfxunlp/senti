local maskRFill, parent = torch.class('nn.maskRFill', 'nn.Module')

function maskRFill:__init(maskid, fillid, prate)
	parent.__init(self)
	self.module = nn.Dropout(prate)
	self.module:training()
	self.maskid = maskid
	self.fillid = fillid
end

function maskRFill:updateOutput(input)

	self._mask = self.module:updateOutput(input:eq(self.maskid):cuda()):cudaByte()
	self.output = input:clone():maskedFill(self._mask, self.fillid)
	return self.output

end
