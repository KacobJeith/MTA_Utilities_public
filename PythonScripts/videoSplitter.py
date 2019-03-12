import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, required=True, help='video file')
parser.add_argument('--csv', type=str, required=True, help='csv label file')
args = parser.parse_args()

class BusData:
	def __init__(self, realTime, relativeTime, stateNumber, stateName) :
		self.realTime = realTime
		self.relativeTime = relativeTime
		self.stateNumber = stateNumber
		self.stateName = stateName

def getCSVData() :

  fname = args.csv

  BusDataList = []

  with open(fname, 'r') as f:
      content = f.readlines()
      for x in range(0, len(content)) :
        splitValue = content[x].split(',')
        if(len(splitValue) == 4) :
          BusDataList.append(BusData(splitValue[0], float(splitValue[1]), int(splitValue[2]), splitValue[3]))
  
  return BusDataList

def readVideo() :
  
  vidcap = cv2.VideoCapture(args.video)
  success,image = vidcap.read()

  filename = args.video.split('.')[0]
  print('Watching ', filename)

  folder = "./{}".format(filename)

  if (os.path.isdir(folder) == False) :
      os.mkdir(folder)

  count = 0
  while success:
    savepath = "./{}/frame_{}.jpg".format(filename, count)
    # cv2.imwrite(savepath, image)     # save frame as JPEG file      
    success,image = vidcap.read()
  #   print('Read a new frame: ', success)
    count += 1


readVideo()