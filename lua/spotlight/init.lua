local Module = {}

local defaultOptions = {
	model = "mistral",
}
for key, value in pairs(defaultOptions) do
	Module[key] = value
end

Module.setup = function(options)
	for key, value in pairs(options) do
		Module[key] = value
	end
end

local function substitutePromptPlaceholders(prompt)
	if not prompt then
		return
	end
	local promptText = prompt
	if string.find(promptText, "%$input") then
		local userPromptResponse = vim.fn.input("Prompt: ")
		promptText = string.gsub(promptText, "%$input", userPromptResponse)
	end
end

Module.exec = function(options)
	local opts = vim.tbl_deep_extend("force", Module, options)

	opts.init(opts)

	local currentBuffer = vim.fn.bufnr("%")
	local mode = opts.mode or vim.fn.mode()
	local startingPosition = nil
	local endingPosition = nil
	if mode == "v" or mode == "V" then
		startingPosition = vim.fn.getpos("'<")
		endingPosition = vim.fn.getpos("'>")
		endingPosition[3] = vim.fn.col("'>")
	else
		startingPosition = vim.fn.getpos(".")
		endingPosition = startingPosition
	end
	local context = table.concat(
		vim.api.nvim_buf_get_text(
			currentBuffer,
			startingPosition[2] - 1,
			startingPosition[3] - 1,
			endingPosition[2] - 1,
			endingPosition[3] - 1,
			{}
		)
	)
end
