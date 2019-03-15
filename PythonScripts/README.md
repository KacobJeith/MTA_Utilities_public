# How to use these Scripts

This folder contains all the scripts needed to perform at-scale nearest neighbor (KNN) cassification of single-frame events on MTA video footage. 

There are four steps in total to training and using this toolset: 
1. Label videos
2. Prepare labeled frames
3. Train the model
4. Use the model


### Labeling videos using the Labeling tool

Video labeling is probably the most important piece of the model training process. Garbage in = garbage out. The quality of a model is only as good as the standard it is striving to match! Head over the Dylan's Unity tool to learn more about the labeling UI features and how-to. The output from that UI is needed for the retraining step of these scripts. 


### Preparing labeled frames

First, you'll need to set up a virtual environment to execute your python scripts. This README will assume you are working on the KACOBDESKTOP machine currently located at NewLab, which already has python, anaconda, GPU libraries, etc set up in their entirety for GPU-boosted machine learning. Yes - it is a bit insane to cater a how-to guide to a specific machine, but it's a starting point! 



##### 1. Activate the GPU-enabled  virtual environment

```
~$ activate tf_gpu
```
This command tells your bash to execute with the python context set up for GPU. tf stands for tensorflow, and gpu stands for...GPU. After you run this, if you are working in a quality bash, your command line should indicate that a python virtual environment is active. In the cmder bash, it looks like: 
```
~(tf_gpu)$ 
```

##### 2. Split the video 
First you need to convert the video into labeled frames. The script for this is MTA_Utilities/PythonScripts/videoSplitter.py. For a list of input parameters, type python videoSplitter.py -h
```
~(tf_gpu)$ python videoSplitter.py -h
usage: videoSplitter.py [-h] --video VIDEO --dataset_name DATASET_NAME --csv
                        CSV

optional arguments:
  -h, --help            show this help message and exit
  --video VIDEO         video file
  --dataset_name DATASET_NAME
                        name of the dataset to save these labels to
  --csv CSV             csv label file


```
All you need to do to run this script is input a path to a video file, the name of a folder to save the labeled frames to, and the path to the CSV file indicating all the labels for the frames. 

### Training the classifier

### Using the model



