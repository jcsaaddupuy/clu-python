#!/usr/bin/env python2
from clu.rabbitmq.common.base import RabbitAgent
import mpd

class MpdAgent(RabbitAgent):
  def __init__(self, *args, **kwargs):
    RabbitAgent.__init__(self, *args, **kwargs)
    self.__nonenables__(("host","port", "user", "password"))
    self.mpd=mpd.MPDClient()

  def connect_mpd():
    self.mpd.connect(self.host, self.port)
    if self.host is not None:
      self.mpd.password(self.password)



class MpdControl(MpdAgent):
  def __init__(self, *args, **kwargs):
    MpdAgent.__init__(self, *args, **kwargs)
  

class MpdStatus(MpdAgent):
  def __init__(self, *args, **kwargs):
    MpdAgent.__init__(self, *args, **kwargs)
