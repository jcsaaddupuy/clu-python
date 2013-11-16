#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.common.base import CluException

from clu.rabbitmq.common.base import RabbitAgent
import mpd

class MpdAgentException(CluException):
  pass

class MpdAgent(Configurable):
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":6600, "password":None}
    self.__defaults__(defaults)

    self.mpd=mpd.MPDClient()

  def connect_mpd(self):
    try:
      self.mpd.connect(self.config.host, self.config.port)
      if self.config.password is not None:
        self.mpd.password(self.config.password)
    except mpd.ConnectionError, e:
      raise MpdAgentException("Connection error", e)
    except mpd.CommandError, e2:
      raise MpdAgentException("Authentcation error", e2)

  def run(self):
    raise MpdAgentException("Not implemented")

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
