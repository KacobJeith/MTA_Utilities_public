class Coordinate:
    def __init__(self, latitude, longitude) :
        self.latitude = latitude
        self.longitude = longitude

class ObstructionPeriod : 
    def __init__(self, severity, startTime, endTime, visionStates, coordinates, doorStates, headings, speeds, accelerations) :
        self.severity = severity
        self.startTime = startTime
        self.endTime = endTime
        self.visionStates = visionStates
        self.coordinates = coordinates
        self.doorStates = doorStates
        self.headings = headings
        self.speeds = speeds
        self.accelerations = accelerations

    def GetCSVString(self) :
        obstructionString = str(self.startTime) + ","
        obstructionString += str(self.endTime) + ","
        obstructionString += str(self.severity) + ","

        for x in range(0, len(self.visionStates)) :
            obstructionString += str(self.visionStates[x]) + ","
            obstructionString += str(self.coordinates[x].longitude) + ","
            obstructionString += str(self.coordinates[x].latitude) + ","
            obstructionString += str(self.doorStates[x]) + ","
            obstructionString += str(self.headings[x]) + ","
            obstructionString += str(self.speeds[x]) + ","
            obstructionString += str(self.accelerations[x]) + ","

        return obstructionString

def GetObstructionPeriodFromString(theString) :
    splitString = theString.split(',')

    startTime = splitString[0]
    endTime = splitString[1]
    severity = int(splitString[2])

    visionStates = []
    coordinates = []
    doorStates = []
    headings = []
    speeds = []
    accelerations = []

    counter = 3
    for x in range(0, severity) :
        visionStates.append(int(splitString[counter])) 
        counter += 1
        latitude = float(splitString[counter])
        counter += 1
        longitude = float(splitString[counter])
        coordinates.append(Coordinate(latitude, longitude))
        counter += 1
        doorStates.append(int(splitString[counter]))
        counter += 1
        headings.append(float(splitString[counter]))
        counter += 1
        speeds.append(float(splitString[counter]))
        counter += 1
        accelerations.append(float(splitString[counter]))
        counter += 1

    return ObstructionPeriod(severity, startTime, endTime, visionStates, coordinates, doorStates, headings, speeds, accelerations)