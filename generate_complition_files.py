import inspect as insp
import sys, os
import shutil
import re

class GetPythonObject():
    
    exportDir = None
    pythonSDKDir = None
    nbdir = 0
    nbfile = 0
    nbline = 0
    def __init__(self):
        self.pythonSDKDir = "/Volumes/Stock_01/Users/valkaari/Documents/Developpement/HTML SDK/CINEMA4DR16021PYTHONSDKHTML20141003/help/modules"
        self.exportDir = "/Volumes/Stock_01/Users/valkaari/Desktop/c4dPython"
        
   
    def exportModule(self, folder):
    
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
                pattern = re.compile(r'<tt class="descclassname">(.+)<a')
                cleanhtml = re.compile('<.*?>')
                for i, line in enumerate(open(os.path.join(folder , fname), "r")):
                    match = re.findall(pattern, line)
                    if match:
                        cleanFunction = re.sub(cleanhtml, '',match[0])
                        cleanFunction = cleanFunction.replace("&quot;" , "\"")
                        patParam = re.compile(r'\(.+\)')
                        parameters = re.search(patParam, cleanFunction)

                        if not parameters:
                            parameters = ""
                        else:
                            parameters = parameters.group()

                        
                        fn.write ("\t\t\t\t{\"trigger\": \"" + str(cleanFunction)   + "\", \"contents\" : \"" + self.funcParser(cleanFunction.split('.')[-1])  +  "\"},\n")
    
                        self.nbline+=1

                #before closing, add a dummy elmt
                fn.write("  \t\t\t\t{ \"trigger\": \"____zzzzzdummy\", \"contents\": \"_____zzzzzdummy\" } ")
                self.nbline+=1
                fn.write ("\n\t\t]\n}")
                self.nbline+=1        
                fn.close()

    def funcParser(self, funcToParse):
        
        # this function add special syntax for sublime to the parameters.
        res  = re.sub(r'(\w+?,|\w+?\[|\w+?\))', r'{}:\1' , funcToParse)
        res  = re.sub(r'(\[.+?\])', r' {}:\1' , res)
        res  = res.format(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50)
        res  = re.sub(r'(\d:\w+|\d:\[.+?\])' , r'${\1}', res)   
        res  = re.sub('"', r'\"', res)
        return res


    def deleteDirectory(self):
        dirlist = os.listdir(self.exportDir)
        for fname in dirlist:
            if os.path.isdir(os.path.join(self.exportDir , fname)):
                shutil.rmtree(os.path.join(self.exportDir, fname))
            else:
                os.remove(os.path.join(self.exportDir, fname))

    def test(self, folder = None):
        if not folder:
            folder = self.pythonSDKDir

        dirList=os.listdir(folder)
        for fname in dirList:
           if os.path.isdir(os.path.join(folder , fname)):
                #if this is a directory, create the directory
                print os.path.join(folder , fname)[len(self.pythonSDKDir):]
                #and go sub folder
                self.test(os.path.join(folder , fname))


    def getStat(self):
        print "nombre de fichiers : " ,self.nbfile
        print "nombre de repertoires : ", self.nbdir
        print "nombre de lignes : ", self.nbline

def main():
    print "let's go"
    getObjects = GetPythonObject()
    #getObjects.test()
    getObjects.deleteDirectory()
    getObjects.exportModule("/Volumes/Stock_01/Users/valkaari/Documents/Developpement/HTML SDK/CINEMA4DR16021PYTHONSDKHTML20141003/help/modules")
    getObjects.getStat()    

    
    print "done"
    
    


    
if __name__=='__main__':
    main()
