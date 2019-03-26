import glob   
from DataTypes import Coordinate
from DataTypes import ObstructionPeriod
from DataTypes import GetObstructionPeriodFromString
from statistics import median
from collections import Counter

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

totalUnkown = 0
totalTrafficLights = 0
totalBusStops = 0
totalObstructions = 0

totalUnknownSeverity = 0
totalTrafficLightSeverity = 0
totalBusStopSeverity = 0
totalObstructedSeverity = 0

# Use modes to determine vision state
for x in range(0, len(masterObstructionList)) :
    d_mem_count = Counter(masterObstructionList[x].visionStates)
    max = 0
    currentMode = 0
    for k in d_mem_count.keys():
        if d_mem_count[k] > max :
            max = d_mem_count[k]
            currentMode = k

    if currentMode == 1 :
        totalUnkown += 1
        totalUnknownSeverity += masterObstructionList[x].severity
    elif currentMode == 2 :
        totalBusStops += 1
        totalBusStopSeverity += masterObstructionList[x].severity
    elif currentMode == 3 :
        totalTrafficLights += 1
        totalTrafficLightSeverity += masterObstructionList[x].severity
    elif currentMode == 4 :
        totalObstructions += 1
        totalObstructedSeverity += masterObstructionList[x].severity

print("Total Unkown Events: " + str(totalUnkown))
print("Total Bus Stop Events: " + str(totalBusStops))
print("Total Traffic Light Events: " + str(totalTrafficLights))
print("Total Obstruction Events: " + str(totalObstructions))
print()
print("Total Unkown Cost: " + str(totalUnknownSeverity))
print("Total Bus Stop Cost: " + str(totalBusStopSeverity))
print("Total Traffic Light Cost: " + str(totalTrafficLightSeverity))
print("Total Obstruction Cost: " + str(totalObstructedSeverity))
print()
print("Average Unkown Cost: " + str(totalUnknownSeverity/totalUnkown))
print("Average Bus Stop Cost: " + str(totalBusStopSeverity/totalBusStops))
print("Average Traffic Light Cost: " + str(totalTrafficLightSeverity/totalTrafficLights))
print("Average Obstruction Cost: " + str(totalObstructedSeverity/totalObstructions))
   
    