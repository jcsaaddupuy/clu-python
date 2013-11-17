#!/usr/bin/env python2
from clu.common.base import Configurable

from clu.agents import CluAgent, CluAgentException
from clu.rabbitmq.common.base import WhiteRabbit
import mpd

class MpdAgentException(CluAgentException):
  pass

class MpdAgent(Configurable):
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
      raise MpdAgentException("Connection error", connex)
    except mpd.CommandError, authex:
      raise MpdAgentException("Authentcation error", authex)
    except mpd.MPDError, unknownex:
      raise MpdAgentException("Authentcation error", unknownex)
  

class MpdRmqAgent(CluAgent):
  def __init__(self, mpdconf={}, rmqconf={}):
    CluAgent.__init__(self)
    self.mpdagent=MpdAgent(mpdconf)
    self.rmqagent=WhiteRabbit(rmqconf)
    
  def before_execute(self):
    self.mpdagent.connect()
    self.rmqagent.connect()

  def after_execute(self):
    self.mpdagent.disconnect()
    self.rmqagent.disconnect()

class MpdControlAgent(MpdRmqAgent):
  def __init__(self, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, mpdconf, rmqconf)
  

class MpdStatusAgent(MpdRmqAgent):
  def __init__(self, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, mpdconf, rmqconf)

  def run(self):
    pass
