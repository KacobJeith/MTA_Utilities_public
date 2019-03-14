import sys

class BusData:
	def __init__(self, realTime, relativeTime, stateNumber, stateName) :
		self.realTime = realTime
		self.relativeTime = relativeTime
		self.stateNumber = stateNumber
		self.stateName = stateName

fname = sys.argv[1]

BusDataList = []

with open(fname, 'r') as f:
    content = f.readlines()
    for x in range(0, len(content)) :
    	splitValue = content[x].split(',')
    	if(len(splitValue) == 4) :
    		BusDataList.append(BusData(splitValue[0], float(splitValue[1]), int(splitValue[2]), splitValue[3]))


# Print the State Names from The data
for x in range(0, len(BusDataList)) :
	print(BusDataList[x].stateName)
	print(x)