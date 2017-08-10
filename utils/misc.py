from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

import tensorflow as tf


def get_scale(tensor):
  assert isinstance(tensor, tf.Tensor)
  return tensor.get_shape().as_list()[1:]


def shape_string(shape):
  assert isinstance(shape, list)
  strs = [str(x) if x is not None else "?" for x in shape]
  return "x".join(strs)


def convert_to_one_hot(labels, classes):
  labels = np.array(labels)
  if len(labels.shape) < 2:
    sample_num = labels.shape[0]
    onehot = np.zeros(shape=[sample_num, classes])
    onehot[range(sample_num), labels] = 1
  else:
    onehot = labels

  if len(onehot.shape) != 2:
    raise ValueError('!! Input labels has an illegal dimension {}'.format(
      len(labels.shape)))

  return onehot




