#!/usr/bin/env python2
from clu.rabbitmq.common.base import WhiteRabbit

class MpdController(WhiteRabbit):
  def __init__(self, **kwargs):
    WhiteRabbit.__init__(self, kwargs)
