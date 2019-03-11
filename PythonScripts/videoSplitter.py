import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, required=True, help='video file')
args = parser.parse_args()

vidcap = cv2.VideoCapture(args.video)
success,image = vidcap.read()
count = 0

filename = args.video.split('.')[0]

print('Processing ', filename)

folder = "./{}".format(filename)

if (os.path.isdir(folder) == False) :
    os.mkdir(folder)

while success:
  savepath = "./{}/frame_{}.jpg".format(filename, count)
  cv2.imwrite(savepath, image)     # save frame as JPEG file      
  success,image = vidcap.read()
#   print('Read a new frame: ', success)
  count += 1