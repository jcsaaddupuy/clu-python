#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

import mpd

class MusicPlayeraemonEception(CluAgentException):
  pass

class MusicPlayerDaemon(Configurable):
  """
  MPD client handler
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":6600, "password":None}
    self.__defaults__(defaults)

    self.mpd=mpd.MPDClient()

  def connect(self):
    try:
      self.mpd.connect(self.config.host, self.config.port)
      if self.config.password is not None:
        self.mpd.password(self.config.password)
    except mpd.ConnectionError, connex:
      raise MusicPlayeraemonEception("Connection error on connect", connex)
    except mpd.CommandError, authex:
      raise MusicPlayeraemonEception("Authentcation error on connect", authex)
    except mpd.MPDError, unknownex:
      raise MusicPlayeraemonEception("Unknown MPD error on connect", unknownex)
  
  def disconnect(self):
    try:
      self.mpd.disconnect()
    except mpd.MPDError, mpdexcept:
      raise MusicPlayeraemonEception("MPD Error on disconnect", mpdexcept)

  
class MpdRmqAgent(RabbitMqAgent):
  def __init__(self, config, mpdconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.mpdagent=MusicPlayerDaemon(mpdconf)
    
    
  def before_execute(self):
    RabbitMqAgent.before_execute(self)
    self.mpdagent.connect()

  def after_execute(self):
    RabbitMqAgent.after_execute(self)
    self.mpdagent.disconnect()

  def mpdclient(self):
    return self.mpdagent.mpd

