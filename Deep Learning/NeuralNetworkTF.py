import cv2
import tensorflow as tf 
import numpy as np
print("OpenCV Version: " + cv2.__version__)
print("Numpy Version: " + np.version.version)
print("Tensorflow Version: " + tf.version.VERSION)

device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
    raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))