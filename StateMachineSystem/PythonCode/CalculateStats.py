import glob   
from DataTypes import Coordinate
from DataTypes import ObstructionPeriod
from DataTypes import GetObstructionPeriodFromString

def IsOutputFile(filename) :
    fileNameSplit = filename.split("_")

    if(len(fileNameSplit) == 2) :
        extensionSplit = fileNameSplit[1].split('.')
        
        if extensionSplit[0] == 'output' :
            return True

    return False

masterObstructionList = []

path = './*.csv'  
files=glob.glob(path)   
for file in files:    
    if IsOutputFile(file) :
        with open(file, 'r') as f:
            content = f.readlines()
            for x in range(0, len(content)) :
                masterObstructionList.append(GetObstructionPeriodFromString(content[x]))
