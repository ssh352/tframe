from __future__ import absolute_import

import tensorflow as tf

from .layer import Layer
from .layer import single_input

from tensorflow.python.layers.pooling import MaxPool2D as MaxPool2D_


class MaxPool2D(MaxPool2D_, Layer):
  """"""
  full_name = 'maxpool2d'

  @single_input
  def __call__(self, input_):
    assert isinstance(input_, tf.Tensor)
    return MaxPool2D_.__call__(self, input_, scope=self.full_name)