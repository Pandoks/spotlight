local Scan = require("plenary.scandir")
local Job = require("plenary.job")
local Telescope = require("telescope.builtin")
local Module = {}

local defaultOptions = {
	ollamaModel = "mistral",
	persist = true,
	pythonPath = "python",
	databaseDirectory = ".nvim-spotlight",
	hidden = true,
	gitignore = true,
	queryNumber = 10,
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
			if vim.fn.isdirectory(directoryLocation .. "/" .. item) == 1 and item == opts.databaseDirectory then
				isInitialized = true
				break
			end
		end

		if isInitialized then
			print("Initialized")
			local prompt = vim.fn.input("Prompt: ")
			local output = nil
			Job:new({
				command = opts.pythonPath,
				args = {
					embeddings,
					"retrieve",
					"--db-location",
					directoryLocation .. "/" .. opts.databaseDirectory,
					"--collection-name",
					"spotlight",
					"--model",
					opts.ollamaModel,
					"--result-amount",
					opts.queryNumber,
				},
				writer = prompt,
				on_exit = function(job)
					output = job:result()[1]
				end,
			}):sync()

			local queryOutput = vim.json.decode(output)
			local files = queryOutput.metadatas[1]
			local fileList = {}
			for _, file in ipairs(files) do
				print(file.file)
				table.insert(fileList, file.file)
			end

			Telescope.find_files({
				prompt_title = "test",
				cwd = vim.fn.getcwd(),
				search_dirs = fileList,
				attach_mappings = function(_, map)
					map("i", "<CR>", function(prompt_bufnr)
						local selection = require("telescope.actions.state").get_selected_entry(prompt_bufnr)
						require("telescope.actions").close(prompt_bufnr)
						vim.api.nvim_command("edit " .. selection.path)
					end)
					return true
				end,
			})
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
				if options.gitignore and (filePath:find("%.git/") or filePath:find("/.git$")) then
					goto continue
				end

				local databaseDirectoryMatchPattern =
					opts.databaseDirectory:gsub("([%%%^%$%(%)%.%[%]%*%+%-%?])", "%%%1")
				if filePath:find(databaseDirectoryMatchPattern .. "/") then
					goto continue
				end

				local file = io.open(filePath, "r")
				if not file then
					goto continue
				end
				local content = file:read("*all")
				file:close()
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
				local handle = io.popen(insertCommand, "w")
				if not handle then
					goto continue
				end
				handle:write(content)
				handle:close()

				::continue::
			end
		end
	end
end

vim.api.nvim_create_user_command("Spotlight", function()
	Module.exec(defaultOptions)
end, {})

return Module
