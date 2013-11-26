""" Class containing Telnet/RabbitMq  classes"""
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from telnetclient import TelnetClient

class TelnetRmqAgenException(Exception):
  """
  Exceptions raised by TelnetRmqAgenException
  """
  pass

class TelnetRmqAgent(RabbitMqAgent):
  """
  Telnet/RabbitMq client handler
  """
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
    except Exception, ex:
      raise TelnetRmqAgenException(ex)
    finally:
      try:
        self.telnet.disconnect()
      except Exception, ex2:
        raise TelnetRmqAgenException(ex2)


  def telnetclient(self):
    return self.telnet.client
