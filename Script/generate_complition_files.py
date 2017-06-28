import sys, os, getopt
import argparse
import shutil
import re
import time

class GetPythonObject():
    
    exportDir = None
    pythonSDKDir = None
    nbdir = 0
    nbfile = 0
    nbline = 0
    def __init__(self,inputDirectory, outputDirectory):
        self.pythonSDKDir = inputDirectory
        self.exportDir = outputDirectory
       
   
    def exportModule(self, folder = ""):
        if folder == "":
            folder = self.pythonSDKDir
        dirList=os.listdir(folder)
      
        for fname in dirList:
            if os.path.isdir(os.path.join(folder , fname)):
                #if this is a directory, create the directory
                os.makedirs (os.path.join(self.exportDir , os.path.join(folder , fname)[len(self.pythonSDKDir)+1:]))
                self.nbdir +=1
                #and go sub folder
                self.exportModule(os.path.join(folder , fname))

            else:
                #create the file
                fn = open(os.path.join(self.exportDir , os.path.join(folder)[len(self.pythonSDKDir)+1:],os.path.basename(folder)+".sublime-completions"),"w")
                self.nbfile +=1
                # write the start 
                fn.write("{\n\t\t\"scope\" : \"source.pythonAPI.cinema4D\",\n\t\t\"completions\" : [\n ")

                #load file in a string
                pattern = re.compile(r'<code class="descclassname">(.+)<a')
                cleanhtml = re.compile('<.*?>')
                for i, line in enumerate(open(os.path.join(folder , fname), "r")):
                    match = re.findall(pattern, line)
                    if match:
                        cleanFunction = re.sub(cleanhtml, '',match[0])
                        cleanFunction = cleanFunction.replace("&quot;" , "\\\"")
                        patParam = re.compile(r'\(.+\)')
                        parameters = re.search(patParam, cleanFunction)

                        if not parameters:
                            parameters = ""
                        else:
                            parameters = parameters.group()

                        
                        fn.write ("\t\t\t\t{\"trigger\": \"" + str(cleanFunction)   + "\", \"contents\" : \"" + self.funcParser(cleanFunction.split('.')[-1])  +  "\"},\n")
    
                        self.nbline+=1

                #before closing, add a dummy elmt
                fn.write("  \t\t\t\t{ \"trigger\": \"____zdummy\", \"contents\": \"_____zdummy\" } ")
                self.nbline+=1
                fn.write ("\n\t\t]\n}")
                self.nbline+=1        
                fn.close()

    def funcParser(self, funcToParse):
        
        # this function add special syntax for sublime to the parameters.
        res  = re.sub(r'(\w+?,|\w+?\[|\w+?\))', r'{}:\1' , funcToParse)
        res  = re.sub(r'(\[.+?\])', r' {}:\1' , res)
        res  = res.format(*list(i for i in range(1,50)))
        res  = re.sub(r'(\d:\w+|\d:\[.+?\])' , r'${\1}', res)   
        #res  = re.sub('"', r'\"', res) 
        return res


    def deleteDirectory(self):
        dirlist = os.listdir(self.exportDir)
        for fname in dirlist:
            if os.path.isdir(os.path.join(self.exportDir , fname)):
                shutil.rmtree(os.path.join(self.exportDir, fname))
            else:
                os.remove(os.path.join(self.exportDir, fname))




    def getStat(self):
        print "files : " ,self.nbfile
        print "directories : ", self.nbdir
        print "lines  : ", self.nbline

def main(args):
    start_time = time.time()
    getObjects = GetPythonObject(args.inputDirectory, args.outputDirectory)
    getObjects.deleteDirectory()
    getObjects.exportModule()
    getObjects.getStat()    

    print ("done in %s seconds" % (time.time() - start_time))
    


    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Create Sublime Package from Cinema4D\'s documentation' )
    parser.add_argument("inputDirectory",help = "the cinema4D's python SDK help directory doc->html->modules")
    parser.add_argument("outputDirectory", help = "The directory to store the result")
    args = parser.parse_args()
    main(args)