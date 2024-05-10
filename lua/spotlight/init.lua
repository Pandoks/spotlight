local Module = {}

Module.setup = function(options)
	for key, value in pairs(options) do
		Module[key] = value
	end
end
