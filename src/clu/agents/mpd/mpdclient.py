#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

import mpd

class MpdClientEception(CluAgentException):
  pass

class MpdClient(Configurable):
  """
  MPD client handler
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":6600, "password":None}
    self.__defaults__(defaults)

    self.client=mpd.MPDClient()

  def connect(self):
    try:
      self.client.connect(self.config.host, self.config.port)
      if self.config.password is not None:
        self.client.password(self.config.password)
    except mpd.ConnectionError, connex:
      raise MpdClientEception("Connection error on connect", connex)
    except mpd.CommandError, authex:
      raise MpdClientEception("Authentcation error on connect", authex)
    except mpd.MPDError, unknownex:
      raise MpdClientEception("Unknown MPD error on connect", unknownex)
  
  def disconnect(self):
    try:
      self.client.disconnect()
    except mpd.MPDError, mpdexcept:
      raise MpdClientEception("MPD Error on disconnect", mpdexcept)
