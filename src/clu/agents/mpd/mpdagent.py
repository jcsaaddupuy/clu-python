#!/usr/bin/env python2
from clu.agents import ConfigurableCluAgent, CluAgentException
from clu.rabbitmq.common.base import RabbitAgent
import mpd

class MpdAgentException(CluAgentException):
  pass

class MpdAgent(ConfigurableCluAgent):
  def __init__(self, config={}):
    ConfigurableCluAgent.__init__(self, config)
    defaults={"host":"localhost", "port":6600, "password":None}
    self.__defaults__(defaults)

    self.mpd=mpd.MPDClient()

  def connect_mpd(self):
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
  

class MpdRmqAgent(object):
  def __init__(self, mpdconf={}, rmqconf={}):
    self.mpdagent=MpdAgent(mpdconf)
    self.rmqagent=RabbitAgent(rmqconf)


class MpdControlAgent(MpdRmqAgent):
  def __init__(self, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, mpdconf, rmqconf)
  

class MpdStatusAgent(MpdRmqAgent):
  def __init__(self, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, mpdconf, rmqconf)

  def run(self):
    pass
