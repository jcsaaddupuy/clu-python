#!/usr/bin/env python2

import pika

from clu.common.base import Configurable

class WhiteRabbit(Configurable):
  def __init__(self, *args, **kwargs):
    Configurable.__init__(self,*args, **kwargs)
    self.__nonenables__(("host","port","password"))

    self._connection=None
    self._connectionParams = None
    self._channel = None

    self.__init_connection_params__()
  
  def __init_connection_params__(self):
    self._connectionParams= pika.ConnectionParameters(self.host)
  
  def connection(self):
    if self._connection is None:
      if self.host is not None:
        self._connection = pika.BlockingConnection(self._connectionParams)
    return self._connection

  def channel(self):
    return self.connection().channel()



class RabbitAgent(Configurable):
  def __init__(self, *args, **kwargs):
    Configurable.__init__(self, *args,**kwargs)
    self.__nonenables__(("rmq_host","rmq_port","rmq_password"))
    rabbit = WhiteRabbit(host=self.rmq_host, port=self.rmq_port, password=self.rmq_password)
    self.rabbit = rabbit

