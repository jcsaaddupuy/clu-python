""" Class containing Telnet/RabbitMq  classes"""
import logging
LOGGER = logging.getLogger(__name__)
import sys

from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from clu.agents.telnet.telnetclient import TelnetClient

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
    RabbitMqAgent.__init__(self, config, rmqconf)
    self.telnetclient = TelnetClient(telnetconf)
    
  def before_execute(self):
    RabbitMqAgent.before_execute(self)
    self.telnetclient.connect()

  def after_execute(self):
    RabbitMqAgent.after_execute(self)
  
  def ensure_after_execute(self):
    try:
      RabbitMqAgent.ensure_after_execute(self)
    except Exception, ex:
      LOGGER.error("Error calling RabbitMqAgent.ensure_after_execute")
      raise TelnetRmqAgenException, TelnetRmqAgenException(ex), sys.exc_info()[2] # keep stacktrace
    finally:
      try:
        self.telnetclient.disconnect()
      except Exception, ex2:
        LOGGER.error("Error disconnecting telnet client")
        raise TelnetRmqAgenException, TelnetRmqAgenException(ex2), sys.exc_info()[2] # keep stacktrace

