import sys
from datetime import datetime

class SingleObstruction:
	def __init__(self, severity, state, curTime) :
		self.severity = severity
		self.state = state
		self.curTime = curTime

class ObstructionPeriod : 
	def __init__(self, severity, startTime, endTime, visionStates) :
		self.severity = severity
		self.startTime = startTime
		self.endTime = endTime
		self.visionStates = visionStates

class MotionState:
	#Motion State Enumeration
	Stopped = 0
	Accelerating = 1
	Cruising = 2
	Decelerating = 3

	def __init__(self, stateType, transitionFunction) :
		self.stateType = stateType
		self.transitionFunction = transitionFunction

	def RunStateMachine(self, acceleration, speed) :
		return self.transitionFunction(acceleration, speed)

	def GetStateType(self) :
		return self.stateType

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



## Capture The Information
# lastState = states[0]
# inObstruction = False

# currentSeverity = 0

# singleObstructionEventList = []
# allObstructions = []

# for x in range(1, len(speeds)) :
# 	acceleration = speeds[x] - speeds[x-1]

# 	if acceleration > 0 :
# 		if inObstruction :
# 			singleObstructionEventList.append(SingleObstruction(currentSeverity, states[x], times[x]))
# 			allObstructions.append(singleObstructionEventList)

# 		inObstruction = False
# 		currentSeverity = 0
# 		singleObstructionEventList = []

# 	else : # Detecting an obstruction
		
# 		currentSeverity += 1

# 		if states[x] != lastState or not inObstruction :
# 			singleObstructionEventList.append(SingleObstruction(currentSeverity, states[x], times[x]))

# 		lastState = states[x]

# 		if not inObstruction :
# 			inObstruction = True
		

## Print Things
# for x in range(0, len(allObstructions)) :
# 	toPrintStr = ""
# 	for y in range(0, len(allObstructions[x])) :
# 		toPrintStr += allObstructions[x][y].curTime + ",  " + str(allObstructions[x][y].severity) + "," + str(allObstructions[x][y].state) + ":  "
# 		print(toPrintStr)


def StoppedTransitionFunction(acceleration, speed) :
	if acceleration > 0 :
		return MotionState.Accelerating

def AcceleratingTransitionFunction(acceleration, speed) :
	if acceleration < 0 :
		return MotionState.Decelerating
	elif acceleration == 0 :
		return MotionState.Cruising

def DeceleratingTransitionFunction(acceleration, speed) :
	if acceleration > 0 :
		return MotionState.Accelerating
	elif acceleration == 0 and speed > 0 :
		return MotionState.Cruising
	elif acceleration == 0 and speed == 0 :
		return MotionState.Stopped

def CruisingTransitionFunction(acceleration, speed) :
	if acceleration < 0 :
		return MotionState.Decelerating
	elif acceleration > 0 :
		return MotionState.Accelerating

StoppedState = MotionState(MotionState.Stopped, StoppedTransitionFunction)
AcceleratingState = MotionState(MotionState.Accelerating, AcceleratingTransitionFunction)
DeceleratingState = MotionState(MotionState.Decelerating, DeceleratingTransitionFunction)
CruisingState = MotionState(MotionState.Cruising, CruisingTransitionFunction)

## Use State Machine
currentSeverity = 0

allObstructions = []

obstructionStartTime = ""
obstructionVisionStates = []

if speeds[0] > 0 :
	currentMotionState = CruisingState
else :
	currentMotionState = StoppedState

for x in range(1, len(speeds)) :
	acceleration = speeds[x] - speeds[x-1]

	prevState = currentMotionState.GetStateType()
	nextState = currentMotionState.RunStateMachine(acceleration, speeds[x])
	if nextState == MotionState.Stopped :
		currentMotionState = StoppedState
	elif nextState == MotionState.Accelerating :
		currentMotionState = AcceleratingState
	elif nextState == MotionState.Decelerating :
		currentMotionState = DeceleratingState
	elif nextState == MotionState.Cruising :
		currentMotionState = CruisingState

	if currentMotionState.GetStateType() == MotionState.Stopped or currentMotionState.GetStateType() == MotionState.Decelerating :
		currentSeverity += 1
		obstructionVisionStates.append(states[x])

		if prevState != MotionState.Stopped and prevState != MotionState.Decelerating :
			obstructionStartTime = times[x]
	else :
		if prevState == MotionState.Stopped or prevState == MotionState.Decelerating :
			allObstructions.append(ObstructionPeriod(currentSeverity, obstructionStartTime, times[x], obstructionVisionStates))
			obstructionVisionStates = []
			obstructionStartTime = ""
		currentSeverity = 0

## Print Results
for x in range(0, len(allObstructions)) :
	printString = ""
	printString += allObstructions[x].startTime + " - " + allObstructions[x].endTime
	printString += " : " + str(allObstructions[x].severity) + " : "

	for y in range(0, len(allObstructions[x].visionStates)) :
		printString += " " + str(allObstructions[x].visionStates[y])

	print(printString)

	# if acceleration > 0 :
	# 	if inObstruction :
	# 		singleObstructionEventList.append(SingleObstruction(currentSeverity, states[x], times[x]))
	# 		allObstructions.append(singleObstructionEventList)

	# 	inObstruction = False
	# 	currentSeverity = 0
	# 	singleObstructionEventList = []

	# else : # Detecting an obstruction
		
	# 	currentSeverity += 1

	# 	if states[x] != lastState or not inObstruction :
	# 		singleObstructionEventList.append(SingleObstruction(currentSeverity, states[x], times[x]))

	# 	lastState = states[x]

	# 	if not inObstruction :
	# 		inObstruction = True
