import sys
from datetime import datetime

class SingleObstruction:
	def __init__(self, severity, state, curTime) :
		self.severity = severity
		self.state = state
		self.curTime = curTime

class Coordinate:
	def __init__(self, latitude, longitude) :
		self.latitude = latitude
		self.longitude = longitude

class ObstructionPeriod : 
	def __init__(self, severity, startTime, endTime, visionStates, coordinates, doorStates, headings) :
		self.severity = severity
		self.startTime = startTime
		self.endTime = endTime
		self.visionStates = visionStates
		self.coordinates = coordinates
		self.doorStates = doorStates
		self.headings = headings

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
latitudes = []
longitudes = []
states = []
times = []
headings = []
doorStates = []

readFirstLine = False

with open(fname, 'r') as f:
	content = f.readlines()
	for x in range(0, len(content)) :
		splitValue = content[x].split(',')

		if readFirstLine :
			times.append(splitValue[0])
			states.append(int(splitValue[1]))
			speeds.append(float(splitValue[2]))
			latitudes.append(float(splitValue[3]))
			longitudes.append(float(splitValue[4]))
			headings.append(float(splitValue[5]))
			doorStates.append(int(splitValue[6]))
		else :
			readFirstLine = True

## STATE MACHINE TRANSITIONS
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
obstructionCoordinates = []
obstructionDoorStates = []
obstructionHeadings = []

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
		obstructionCoordinates.append(Coordinate(latitudes[x], longitudes[x]))
		obstructionDoorStates.append(doorStates[x])
		obstructionHeadings.append(headings[x])

		if prevState != MotionState.Stopped and prevState != MotionState.Decelerating :
			obstructionStartTime = times[x]
	else :
		if prevState == MotionState.Stopped or prevState == MotionState.Decelerating :
			allObstructions.append(ObstructionPeriod(currentSeverity, obstructionStartTime, times[x], obstructionVisionStates, obstructionCoordinates, obstructionDoorStates, obstructionHeadings))
			obstructionVisionStates = []
			obstructionDoorStates = []
			obstructionCoordinates = []
			obstructionHeadings = []
			obstructionStartTime = ""
		currentSeverity = 0

## Print Results
for x in range(0, len(allObstructions)) :
	printString = ""
	printString += allObstructions[x].startTime + " - " + allObstructions[x].endTime
	printString += " : " + str(allObstructions[x].severity) + " : "
	printString += " : " + str(allObstructions[x].coordinates[0].latitude) + "," + str(allObstructions[x].coordinates[0].longitude)

	for y in range(0, len(allObstructions[x].visionStates)) :
		printString += " " + str(allObstructions[x].visionStates[y])

	print(printString)

