#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mpdclient import MpdClient
import mpd

  
class MpdRmqAgent(RabbitMqAgent):
  def __init__(self, config, mpdconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.mpdagent=MpdClient(mpdconf)
    
    
  def before_execute(self):
    RabbitMqAgent.before_execute(self)
    self.mpdagent.connect()

  def after_execute(self):
    RabbitMqAgent.after_execute(self)
    self.mpdagent.disconnect()

  def mpdclient(self):
    return self.mpdagent.mpd

