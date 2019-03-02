import cv2
import json
import datetime
import progressbar
from pprint import pprint
import webbrowser

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

def initializeFirebase():
    cred = credentials.Certificate('mta-bus-view-9f7792f35032.json')
    print('Initialized Firebase App')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://mta-bus-view.firebaseio.com',
        'storageBucket': 'mta-bus-view.appspot.com'
    })


def downloadFile(filename):
    print 'Downloading Video to temp file...'

    tempName = 'temporaryVideo.mp4'

    storage.bucket('mta-bus-view-originals').blob(filename).download_to_filename(tempName, client=None, start=None, end=None)
    
    print 'Download complete!'
    return tempName

def getColorForObject(description):
    if description == 'car':
        return (0, 255, 0)
    else :
        return (255,0, 0)

def convertTimeToFrameIndex(frameSecondOffset, frameNanoOffset, fps):
    frame = frameSecondOffset*fps + fps*frameNanoOffset/1000000000
    return int(frame)

def addBoxToFrameMetadata(boundingDict, index, metadata):

    if index in boundingDict:
        boundingDict[index].append(metadata)
    else :
        boundingDict[index] = [metadata] 

    return boundingDict


def printRectanglesOnFrame(frame, metadata, width, height):
    # pprint(metadata)
    if 'left' in metadata['box']: 
        left = metadata['box']['left']
    else:
        left = 0;

    if 'top' in metadata['box']: 
        top = metadata['box']['top']
    else:
        top = 0;

    cv2.rectangle(
        frame, 
        (int(left*width), int(top*height)), 
        (int(metadata['box']['right']*width), int(metadata['box']['bottom']*height)), 
        getColorForObject(metadata['description']), 
        2
    )

    cv2.putText(
        frame, 
        metadata['description'],
        (int(left*width), int(top*height)-3), 
        0, 
        .3,
        getColorForObject(metadata['description']), 
        1
    )

def organizeMetadataIntoFrames(data, fps):
    boundingDict = {}

    for detectedObject in data['objectAnnotations']:

        for frame in detectedObject['frames']:
            if 'description' in detectedObject['entity']:
                description = detectedObject['entity']['description']
            else:
                description = 'unknown'

            metadata = {
                'confidence':  detectedObject['confidence'],
                'description': description,
                'box': frame['normalizedBoundingBox']
            }

            if 'timeOffset' in frame :
                if 'seconds' in frame['timeOffset']:
                    if 'nanos' in frame['timeOffset']:
                        index = convertTimeToFrameIndex(frame['timeOffset']['seconds']['low'], frame['timeOffset']['nanos'], fps)
                    else:
                        index = convertTimeToFrameIndex(frame['timeOffset']['seconds']['low'], 0, fps)
                else : 
                    index = convertTimeToFrameIndex(0, frame['timeOffset']['nanos'], fps)

                boundingDict = addBoxToFrameMetadata(boundingDict, str(index), metadata)
                boundingDict = addBoxToFrameMetadata(boundingDict, str(index+1), metadata)
                boundingDict = addBoxToFrameMetadata(boundingDict, str(index+2), metadata)
            else :
                index = 1;

                boundingDict = addBoxToFrameMetadata(boundingDict, str(index), metadata)
                boundingDict = addBoxToFrameMetadata(boundingDict, str(index+1), metadata)
                boundingDict = addBoxToFrameMetadata(boundingDict, str(index+2), metadata)

    return boundingDict

def addAnnotationsToVideo(tempFile, metadata, saveFile):
    print 'Adding annotations to video...'

    

    cap = cv2.VideoCapture(tempFile)
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    boundingDict = organizeMetadataIntoFrames(metadata, fps)

    frameIndex = 0
    video = cv2.VideoWriter(saveFile, cv2.VideoWriter_fourcc(*'avc1'), fps, (int(width),int(height)))

    bar = progressbar.ProgressBar(maxval=length, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    while(1):
       frameIndex += 1
       ret, frame = cap.read()

       if str(frameIndex) in boundingDict:
            for box in boundingDict[str(frameIndex)]:
                printRectanglesOnFrame(frame, box, width, height)

            
       if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
           cap.release()
           video.release()
           cv2.destroyAllWindows()
           bar.finish()
           break

       bar.update(frameIndex+1)
       video.write(frame)
       # cv2.imshow('frame',frame)

    print 'Video Annotating Complete...'

    return 1


def downloadAndProcessVideo(queuedVideo, queueID):
    annotationsPath = 'annotations/' + queuedVideo['annotationsPath']
    gsPath = queuedVideo['gsPath']

    delimiter = '.'
    filenameElements = gsPath.split(delimiter)
    saveFilename = filenameElements[0] + '_annotated' + delimiter + 'mp4'

    metadata = downloadMetadata(annotationsPath)
    tempLocalPath = downloadFile(gsPath)
    addAnnotationsToVideo(tempLocalPath, metadata, saveFilename)
    uploadFileToStorage(saveFilename)
    firebase_admin.db.reference('processQueue/' + queueID).delete();

def downloadMetadata(datapath):
    print 'Downloading Video Metadata...' + datapath
    metadata =  firebase_admin.db.reference(datapath).get()
    return metadata


def listener(event):
    # print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference
    print(event.data)  # new data at /reference/event.path. None if deleted

    if event.path == '/':
        # First read
        for queueID in event.data.keys():
            if queueID != '_empty':
                downloadAndProcessVideo(event.data[queueID], queueID)
    elif event.data == None:
        print 'Data was deleted'
    else:
        # Subsequent Reads
        print 'Hit the else case'
        queueID = event.path
        downloadAndProcessVideo(event.data, queueID)


def uploadFileToStorage(localFilePath):
    print 'Uploading video to Storage...'
    storage.bucket('mta-bus-view-annotated').blob(localFilePath).upload_from_filename(localFilePath)
    print 'Upload complete!'
    openVideoInChrome(localFilePath)

def watchDatabase(path):
    firebase_admin.db.reference(path).listen(listener)

def openVideoInChrome(localFilePath):
    publicURL = storage.bucket('mta-bus-view-annotated').blob(localFilePath).generate_signed_url(datetime.datetime.now() + datetime.timedelta(days=1));
    print publicURL

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(publicURL)

initializeFirebase()
watchDatabase('processQueue')
# openVideoInChrome('nyc1_annotated.mp4')















