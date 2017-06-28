import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    fn = open (c4d.storage.SaveDialog(),"w")
    
  
    fn.write ("- begin: .*(c4d)(\\.)\n")
    fn.write ("\tbeginCaptures:\n")
    fn.write ("\t\t'1': {name: keyword.module.pythonAPI.cinema4D}\n")
    fn.write ("\t\t'2': {name: ponctuation.pythonAPI.cinema4D}\n")
    fn.write ("\tend: ")
    
    
    fn.write("(")
    for line in dir(c4d):
        fn.write (line+"|")
        
    
    fn.write(")\n")    
    fn.write ("\tendCaptures:\n")
    fn.write("\t\t'1': {name: constant.numeric.pythonAPI.cinema4D}\n")
    
        
    fn.close()
    print "ok"
if __name__=='__main__':
    main()
