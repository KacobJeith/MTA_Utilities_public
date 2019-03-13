# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import cv2
import numpy as np
import tensorflow as tf


parser = argparse.ArgumentParser()
parser.add_argument("--video", type=str, required=True, help="video to be processed")
parser.add_argument("--skip_frames", type=int, default=9, help="name of file containing labels")
parser.add_argument("--graph", type=str, default='/tmp/output_graph.pb', help="graph/model to be executed")
parser.add_argument("--labels", type=str, default='/tmp/output_labels.txt', help="name of file containing labels")
parser.add_argument("--input_layer", type=str, default='Placeholder', help="name of input layer")
parser.add_argument("--output_layer", type=str, default='final_result', help="name of output layer")
parser.add_argument("--input_height", type=int, default=299, help="input height")
parser.add_argument("--input_width", type=int, default=299, help="input width")
parser.add_argument("--input_mean", type=int,  default=0, help="input mean")
parser.add_argument("--input_std", type=int,  default=255, help="input std")

args = parser.parse_args()


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def preprocess_image(image,
                            input_height=299,
                            input_width=299,
                            input_mean=0,
                            input_std=255):
    
    img2= cv2.resize(image,dsize=(299,299), interpolation = cv2.INTER_CUBIC)
    np_image_data = np.asarray(img2)
    np_final = np.expand_dims(np_image_data,axis=0)
    np_image_data = cv2.normalize(np_final.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)

    return np_image_data

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


def predictOnVideo() :
    labels = load_labels(args.labels)
    input_name = "import/" + args.input_layer
    output_name = "import/" + args.output_layer

    graph = load_graph(args.graph)
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    vidcap = cv2.VideoCapture(args.video)
    success,image = vidcap.read()
    frameCounter = 0

    busstop = 0
    moving = 0


    with tf.Session(graph=graph) as sess:
        while success :
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameCounter)
            print('FRAME: ', frameCounter)
            success,image = vidcap.read()
            t = preprocess_image(image)

            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: t
            })

            results = np.squeeze(results)
            # print(np.where(results == np.amax(results)))
              
            # top_k = results.argsort()[-5:][::-1]

            # for i in top_k:
            #     print(labels[i], results[i])

            frameCounter += args.skip_frames + 1

# image = get_frame_from_video(args.video)
# display_image(image)
# predictOnImage(image)

predictOnVideo()



