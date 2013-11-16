#!/usr/bin/env python2

import pika

from clu.common.base import Configurable

class WhiteRabbit(Configurable):
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":5672, "user":"guest", "password":"guest"}
    self.__defaults__(defaults)

    self._connection=None
    self._connectionParams = None
    self._channel = None

    self.__init_connection_params__()
  
  def __init_connection_params__(self):
    self._connectionParams= pika.ConnectionParameters(self.config.host)
  
  def connection(self):
    if self._connection is None:
      if self._connectionParams is not None:
        self._connection = pika.BlockingConnection(self._connectionParams)
    return self._connection

  def channel(self):
    return self.connection().channel()



class RabbitAgent(Configurable):
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    rabbit = WhiteRabbit(config)
    self.rabbit = rabbit

