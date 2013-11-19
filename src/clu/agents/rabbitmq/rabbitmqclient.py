#!/usr/bin/env python2

import pika

from clu.common.base import Configurable

class RabbitmqClientException(Exception):
  pass

class RabbitmqClient(Configurable):
  """
  Rabbitmq client handler.
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":5672, "user":"guest", "password":"guest"}
    self.__defaults__(defaults)

    self._connectionParams = None
    self.connection=None
    self.channel = None


  def connect(self):
    try:
      cred=pika.PlainCredentials(self.config.user, self.config.password)
      params= pika.ConnectionParameters(host=self.config.host, port=self.config.port, credentials=cred)
      self.connection = pika.BlockingConnection(params)
      self.channel = self.connection.channel()
    except Exception, e:
      raise RabbitmqClientException(e)

  def disconnect(self):
    try:
      self.connection.close()
    except Exception, e:
      raise RabbitmqClientException(e)
