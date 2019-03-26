import glob   

def IsOutputFile(filename) :
    fileNameSplit = filename.split("_")

    if(len(fileNameSplit) == 2) :
        extensionSplit = fileNameSplit[1].split('.')
        
        if extensionSplit[0] == 'output' :
            return True

    return False

path = './*.csv'  
files=glob.glob(path)   
for file in files:    
    if IsOutputFile(file) :
        print(file)
