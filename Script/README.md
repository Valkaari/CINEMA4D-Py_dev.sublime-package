Generate c4d_modules complitiions files

	generate_complition_files.py will generate c4d_modules files and subdirectories based on python documentation
	in a command line prompt : python generate_complition_files.py source destination
	source = python documentation->doc->html->modules


Generate language synthaxe:

	this is done in two part : 
		1 - get_syntaxe.py will get the first part of the synthax for the cinema4D_pythonAPI.YAML-tmLanguage file
			in a command line prompt : python get_syntaxe.py source destination
			source = python documentation->doc->html->modules
		2 - export_c4d_constants.py have to be executed inside cinema4D to generate the second part (the constants)
			ask for a file to save the informations.

	both part have to be concatanate inside cinema4D_pythonAPI.YAML-tmLanguage files
	After that, this file have to be converted to json via sublime command "PackageDev : Convert (YAML, Json , Plist ) to ..."

