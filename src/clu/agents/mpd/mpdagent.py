#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mpdclient import MpdClient
import mpd

class MpdRmqException(Exception):
  pass
  
class MpdRmqAgent(RabbitMqAgent):
  def __init__(self, config, mpdconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.mpdclient=MpdClient(mpdconf)
    
    
  def before_execute(self):
    self.mpdclient.connect()
    RabbitMqAgent.before_execute(self)
  
  def after_execute(self):
    RabbitMqAgent.after_execute(self)

  def ensure_after_execute(self):
    try:
      RabbitMqAgent.ensure_after_execute(self)
    except Exception, e:
      raise MpdRmqException(e)
    finally:
      try:
        self.mpdclient.disconnect()
      except Exception, e2:
        raise MpdRmqException(e2)

