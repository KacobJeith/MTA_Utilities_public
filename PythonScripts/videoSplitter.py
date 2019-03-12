import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, required=True, help='video file')
parser.add_argument('--dataset_name', type=str, required=True, help='name of the dataset to save these labels to')
parser.add_argument('--csv', type=str, required=True, help='csv label file')
args = parser.parse_args()

class BusData:
	def __init__(self, realTime, relativeTime, stateNumber, stateName) :
		self.realTime = realTime
		self.relativeTime = relativeTime
		self.stateNumber = stateNumber
		self.stateName = stateName

def getCSVData(fname) :
  BusDataList = []

  with open(fname, 'r') as f:
      content = f.readlines()
      for x in range(0, len(content)) :
        splitValue = content[x].split(',')
        if(len(splitValue) == 4) :
          BusDataList.append(BusData(splitValue[0], float(splitValue[1]), int(splitValue[2]), splitValue[3].split('\n')[0]))
  
  return BusDataList

def labelVideo(busdata, datasetName, vidName) :
  
  vidcap = cv2.VideoCapture(args.video)
  success,image = vidcap.read()
  
  count = 0
  while count < 300:
    # 
    success,image = vidcap.read()
    busdata, thisLabel = labelFrame(count, busdata)
    print(thisLabel)
    checkFolders(datasetName, thisLabel)
    savepath = "./{}/{}/{}_{}.jpg".format(datasetName, thisLabel, vidName, count)
    cv2.imwrite(savepath, image)     # save frame as JPEG file      
    count += 1

def checkFolders(datasetName, label) :

  datasetLocation = "./{}".format(datasetName)
  folder = "./{}/{}".format(datasetName, label)

  if (os.path.isdir(datasetLocation) == False) :
      os.mkdir(datasetLocation)

  if (os.path.isdir(folder) == False) :
      os.mkdir(folder)

def labelFrame(frameNumber, busdata) :

  if len(busdata) == 1 :
    return busdata, busdata[0].stateName

  if frameNumber / 30 > busdata[1].relativeTime  : 
    busdata.pop(0)
  
  return busdata, busdata[0].stateName

vidName = os.path.basename(args.video).split('.')[0]

busData = getCSVData(args.csv)
labelVideo(busData, args.dataset_name, vidName)