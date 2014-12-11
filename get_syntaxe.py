import inspect as insp
import sys, os
import shutil
import re

class Stupid():

	pythonSDKDir = ""
	exportDir = ""
	syntaxes = ""
	def __init__(self):
		self.pythonSDKDir = "/Volumes/Stock_01/Users/valkaari/Documents/Developpement/HTML SDK/CINEMA4DR16021PYTHONSDKHTML20141003/help/modules/c4d/index.html"
		self.exportDir = "/Volumes/Stock_01/Users/valkaari/Desktop/c4dPython"

	def getSyntax(self, file):
		#return a string
		searchString = ""
		for line in open(file,'r'):
			searchString +=line

		module = re.search(r'#module-.+? title="(.+?)">' , searchString, re.DOTALL)
		if not module:
			return ""

		moduleName = module.group(1)

		res = re.search(r'<div class="section" id="types">(.+)<div class="section"', searchString, re.DOTALL)
		if not res:
			return ""
		res = re.findall(r'(<li>?.+?|<dt>?.+?)<a class="reference internal" href="(.*?)/index\.html', res.group(1))
		if not res:
			return ""
		myClasses = ""
		for occ in res:
			myClasses += occ[1].split("/")[-1] + "|"

		syntax = ""
		syntax += "- begin: (\\b\."+  re.sub('\.', '\\.', moduleName).split(".")[-1] + "\\b)(\.)\n"
		syntax += "  beginCaptures:\n"
		syntax += "     '1': {name: keyword.module.pythonAPI.cinema4D}\n"
		syntax += "     '2': {name: ponctuation.pythonAPI.cinema4D}\n"
		syntax += "  end: \\b("+ myClasses[:-1] +")\\b\n"
		syntax += "  endCaptures:\n"
		syntax += "     '1': {name: class."+ moduleName.split(".")[-1] +".pythonAPI.cinema4D}\n"

		return syntax

	def createSyntaxes(self, folder):
		dirList=os.listdir(folder)

		for fname in dirList:
			if os.path.isdir(os.path.join(folder , fname)):
				self.createSyntaxes(os.path.join(folder , fname))
			else:
				#get syntax for that file.
				self.syntaxes += self.getSyntax(os.path.join(folder , fname))



def main():
	dummy = Stupid()
	dummy.createSyntaxes("/Volumes/Stock_01/Users/valkaari/Documents/Developpement/HTML SDK/CINEMA4DR16021PYTHONSDKHTML20141003/help/modules")
	print dummy.syntaxes



    
    
if __name__=='__main__':
    main()
