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


def read_tensor_from_image(image,
                            input_height=299,
                            input_width=299,
                            input_mean=0,
                            input_std=255):

    img_str = cv2.imencode('.jpg', image)[1].tostring()
    image_reader = tf.image.decode_jpeg(img_str)
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    # sess = tf.Session()
    # result = sess.run(normalized)

    return normalized

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
    count = 0

    busstop = 0
    moving = 0


    with tf.Session(graph=graph) as sess:
        while success :
            print('FRAME: ', count)
            success,image = vidcap.read()
            # t = read_tensor_from_image(image)
            normalized = read_tensor_from_image(image)
            t = sess.run(normalized)

            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: t
            })

            results = np.squeeze(results)
            print(np.where(results == np.amax(results)))
              

            top_k = results.argsort()[-5:][::-1]

            for i in top_k:
                print(labels[i], results[i])

            count += 1

# image = get_frame_from_video(args.video)
# display_image(image)
# predictOnImage(image)
predictOnVideo()



