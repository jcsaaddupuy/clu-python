#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from xbmcclient import XbmcClient


class XbmcRmqAgent(RabbitMqAgent):
  def __init__(self, config, xbmcconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.xbmc=XbmcClient(xbmcconf)
    
  def before_execute(self):
    RabbitMqAgent.before_execute(self)

  def after_execute(self):
    RabbitMqAgent.after_execute(self)

  def xbmcclient(self):
    return self.xbmc.client
