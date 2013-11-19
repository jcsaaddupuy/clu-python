#!/usr/bin/env python2

from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from telnetclient import TelnetClient

class TelnetRmqAgenException(Exception):
  pass

class TelnetRmqAgent(RabbitMqAgent):
  def __init__(self, config, telnetconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.telnet=TelnetClient(telnetconf)
    
  def before_execute(self):
    RabbitMqAgent.before_execute(self)
    self.telnet.connect()

  def after_execute(self):
    RabbitMqAgent.after_execute(self)
  
  def ensure_after_execute(self):
    ex=None
    try:
      RabbitMqAgent.ensure_after_execute(self)
    except Exception, e:
      raise TelnetRmqAgenException(e)
    finally:
      try:
        self.telnet.disconnect()
      except Exception, e2:
        raise TelnetRmqAgenException(e2)


  def telnetclient(self):
    return self.telnet.client
