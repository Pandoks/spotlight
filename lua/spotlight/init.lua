local Scan = require("plenary.scandir")
local Module = {}

local defaultOptions = {
	ollamaModel = "mistral",
	persist = true,
	pythonPath = "python",
	databaseDirectory = ".nvim-spotlight",
	hidden = true,
	gitignore = false,
}
for key, value in pairs(defaultOptions) do
	Module[key] = value
end

Module.setup = function(options)
	for key, value in pairs(options) do
		Module[key] = value
	end
end

Module.exec = function(options)
	local opts = vim.tbl_deep_extend("force", Module, options)
	local embeddings = vim.api.nvim_get_runtime_file("embeddings.py", true)
	for _, value in ipairs(embeddings) do
		if value:find("spotlight/embeddings.py") ~= nil then
			embeddings = value
			break
		end
	end
	if opts.persist then
		local directoryLocation = vim.fn.getcwd()
		local items = vim.fs.dir(directoryLocation)
		local isInitialized = false
		for item in items do
			if vim.fn.isdirectory(directoryLocation .. item) == 1 and item == opts.databaseDirectory then
				isInitialized = true
				break
			end
		end

		if isInitialized then
			print("test")
		else
			print("Initializing...")
			local setupCommand = opts.pythonPath
				.. " "
				.. embeddings
				.. " setup --db-location "
				.. directoryLocation
				.. "/"
				.. opts.databaseDirectory
				.. " --collection-name spotlight"
			os.execute(setupCommand)
			print("Created vector database at " .. directoryLocation .. "/" .. opts.databaseDirectory)

			print("Uploading codebase to the vector database (this may take some time)")
			local files = Scan.scan_dir(directoryLocation, {
				hidden = options.hidden,
				respect_gitignore = options.gitignore,
			})
			for _, filePath in ipairs(files) do
				local file = io.open(filePath, "r")
				if not file then
					goto continue
				end
				local content = file:read("*all")
				file:close()
				content = content:gsub("\\", "\\\\"):gsub("'", "\\'")
				local insertCommand = opts.pythonPath
					.. " "
					.. embeddings
					.. " store --db-location "
					.. directoryLocation
					.. "/"
					.. opts.databaseDirectory
					.. " --collection-name spotlight --model "
					.. opts.ollamaModel
					.. " --file-location "
					.. filePath
					.. " --text '"
					.. content
					.. "'"
				os.execute(insertCommand)
				::continue::
			end
		end
	end
end

vim.api.nvim_create_user_command("Spotlight", function()
	Module.exec(defaultOptions)
end, {})

return Module
