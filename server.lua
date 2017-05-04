local zmq = require("zmq")
local json = require("dkjson")

require "cutorch"
require "nn"
require "dpnn"
require "dep.vecLookupZero"
require "dep.SeqDropout"
require "cunn"
require "cudnn"

local logd="logs"

require "utils.Logger"
local logger = Logger(logd.."/server.log", nil, nil, "w")

local options = {host='127.0.0.1',
	port='7556',
	model='modrs/170420_0.2_0.2_1_h50_bgrulsoftp_dcrit/devnnmod2.asc'}

local function predictMessage(prem, input)
	local rs = {}
	for _, _bi in ipairs(input) do
		local _i = torch.CudaLongTensor(_bi)
		local pred = prem:updateOutput(_i):float():lshift(8):int():totable()
		table.insert(rs, pred)
	end
	return rs
end

local function main()

	logger:info("Loading model")
	require "serverloader.normal"
	--require "serverloader.sentence"
	local servm = loadmodel(options.model)

	local ctx = zmq.init(1)
	local s = ctx:socket(zmq.REP)

	local url = "tcp://" .. options.host .. ":" .. options.port
	s:bind(url)
	logger:info("Server initialized at " .. url)
	while true do
		-- Input format is a json batch of src strings.
		local recv = s:recv()
		logger:info("Received... " .. recv)
		local message = json.decode(recv)

		local ret
		local _, err = pcall(function ()
			local pv = predictMessage(servm, message)
			ret = json.encode(pv)
		end)

		if err then
			-- Hide paths included in the error message.
			err = err:gsub("/[^:]*/", "")
			ret = json.encode({ error = err })
		end

		s:send(ret)
		logger:info("Returning... " .. ret)
		collectgarbage()
	end
end

main()
