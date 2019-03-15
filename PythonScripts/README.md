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
Now that you have a folder with labeled frames, you can train your KNN model. To keep things efficient and simple, we're currently using a really nice google script to handle all the CV retraining, located in the file retrain.py. Running --help on this file is a bit more intimidating:

```
$ python retrain.py -h
WARNING: Logging before flag parsing goes to stderr.
W0315 18:42:00.449360 140736103768960 __init__.py:56] Some hub symbols are not available because TensorFlow version is less than 1.14
usage: retrain.py [-h] [--image_dir IMAGE_DIR] [--output_graph OUTPUT_GRAPH]
                  [--intermediate_output_graphs_dir INTERMEDIATE_OUTPUT_GRAPHS_DIR]
                  [--intermediate_store_frequency INTERMEDIATE_STORE_FREQUENCY]
                  [--output_labels OUTPUT_LABELS]
                  [--summaries_dir SUMMARIES_DIR]
                  [--how_many_training_steps HOW_MANY_TRAINING_STEPS]
                  [--learning_rate LEARNING_RATE]
                  [--testing_percentage TESTING_PERCENTAGE]
                  [--validation_percentage VALIDATION_PERCENTAGE]
                  [--eval_step_interval EVAL_STEP_INTERVAL]
                  [--train_batch_size TRAIN_BATCH_SIZE]
                  [--test_batch_size TEST_BATCH_SIZE]
                  [--validation_batch_size VALIDATION_BATCH_SIZE]
                  [--print_misclassified_test_images]
                  [--bottleneck_dir BOTTLENECK_DIR]
                  [--final_tensor_name FINAL_TENSOR_NAME] [--flip_left_right]
                  [--random_crop RANDOM_CROP] [--random_scale RANDOM_SCALE]
                  [--random_brightness RANDOM_BRIGHTNESS]
                  [--tfhub_module TFHUB_MODULE]
                  [--saved_model_dir SAVED_MODEL_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --image_dir IMAGE_DIR
                        Path to folders of labeled images.
  --output_graph OUTPUT_GRAPH
                        Where to save the trained graph.
  --intermediate_output_graphs_dir INTERMEDIATE_OUTPUT_GRAPHS_DIR
                        Where to save the intermediate graphs.
  --intermediate_store_frequency INTERMEDIATE_STORE_FREQUENCY
                        How many steps to store intermediate graph. If "0"
                        then will not store.
  --output_labels OUTPUT_LABELS
                        Where to save the trained graph's labels.
  --summaries_dir SUMMARIES_DIR
                        Where to save summary logs for TensorBoard.
  --how_many_training_steps HOW_MANY_TRAINING_STEPS
                        How many training steps to run before ending.
  --learning_rate LEARNING_RATE
                        How large a learning rate to use when training.
  --testing_percentage TESTING_PERCENTAGE
                        What percentage of images to use as a test set.
  --validation_percentage VALIDATION_PERCENTAGE
                        What percentage of images to use as a validation set.
  --eval_step_interval EVAL_STEP_INTERVAL
                        How often to evaluate the training results.
  --train_batch_size TRAIN_BATCH_SIZE
                        How many images to train on at a time.
  --test_batch_size TEST_BATCH_SIZE
                        How many images to test on. This test set is only used
                        once, to evaluate the final accuracy of the model
                        after training completes. A value of -1 causes the
                        entire test set to be used, which leads to more stable
                        results across runs.
  --validation_batch_size VALIDATION_BATCH_SIZE
                        How many images to use in an evaluation batch. This
                        validation set is used much more often than the test
                        set, and is an early indicator of how accurate the
                        model is during training. A value of -1 causes the
                        entire validation set to be used, which leads to more
                        stable results across training iterations, but may be
                        slower on large training sets.
  --print_misclassified_test_images
                        Whether to print out a list of all misclassified test
                        images.
  --bottleneck_dir BOTTLENECK_DIR
                        Path to cache bottleneck layer values as files.
  --final_tensor_name FINAL_TENSOR_NAME
                        The name of the output classification layer in the
                        retrained graph.
  --flip_left_right     Whether to randomly flip half of the training images
                        horizontally.
  --random_crop RANDOM_CROP
                        A percentage determining how much of a margin to
                        randomly crop off the training images.
  --random_scale RANDOM_SCALE
                        A percentage determining how much to randomly scale up
                        the size of the training images by.
  --random_brightness RANDOM_BRIGHTNESS
                        A percentage determining how much to randomly multiply
                        the training image input pixels up or down by.
  --tfhub_module TFHUB_MODULE
                        Which TensorFlow Hub module to use. For more options,
                        search https://tfhub.dev for image feature vector
                        modules.
  --saved_model_dir SAVED_MODEL_DIR
                        Where to save the exported graph.
```

But fear not, all you need to input is the path to the labeled image frames! Here is how I recommend running this file: 

```
~(tf_gpu)$ python retrain.py --image_dir fake_path_to_dir
```

This will launch a pretty lengthy training process. For best results, make sure that for each label you have at minimum 20 example images. I've seen errors if there are fewer than that. The output from retrain.py is shiny new model! There are two files that you will need: output_graph.pb, and output_labels.txt. These are saved to the path C:/tmp/output_graph.pb and C:/tmp/output_labels.txt. I recommend copying these off to a folder in your working directory, because the next time you retrain these files will be overwritten. It's possible that you might have better luck then me trying to use some of the many optional parameters to save your models to other locations


### Using the model



