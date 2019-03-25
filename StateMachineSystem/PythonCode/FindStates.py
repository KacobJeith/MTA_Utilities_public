import sys
from datetime import datetime

class SingleObstruction:
	def __init__(self, severity, state, curTime) :
		self.severity = severity
		self.state = state
		self.curTime = curTime

fname = sys.argv[1]

BusDataList = []

speeds = []
states = []
times = []

readFirstLine = False

with open(fname, 'r') as f:
	content = f.readlines()
	for x in range(0, len(content)) :
		splitValue = content[x].split(',')

		if readFirstLine :
			#times.append(datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'))
			times.append(splitValue[0])
			speeds.append(float(splitValue[2]))
			states.append(int(splitValue[1]))
		else :
			readFirstLine = True

            #print(splitValue[0] + " " + splitValue[1] + " " + splitValue[2])
    		#BusDataList.append(BusData(splitValue[0], float(splitValue[1]), int(splitValue[2]), splitValue[3]))


lastState = states[0]
inObstruction = False

currentSeverity = 0

singleObstructionEventList = []
allObstructions = []

for x in range(1, len(speeds)) :
	acceleration = speeds[x] - speeds[x-1]

	if acceleration > 0 :
		if inObstruction :
			allObstructions.append(singleObstructionEventList)

		inObstruction = False
		currentSeverity = 0
		singleObstructionEventList = []

	else : # Detecting an obstruction
		
		currentSeverity += 1

		if states[x] != lastState or not inObstruction :
			singleObstructionEventList.append(SingleObstruction(currentSeverity, states[x], times[x]))

		lastState = states[x]

		if not inObstruction :
			inObstruction = True
		

for x in range(0, len(allObstructions)) :
	toPrintStr = ""
	for y in range(0, len(allObstructions[x])) :
		toPrintStr += allObstructions[x][y].curTime + ",  " + str(allObstructions[x][y].severity) + "," + str(allObstructions[x][y].state) + ":  "
		print(toPrintStr)


# Print the State Names from The data
# for x in range(0, len(BusDataList)) :
# 	print(BusDataList[x].stateName)
# 	print(x)