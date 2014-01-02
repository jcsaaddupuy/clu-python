import logging
LOGGER = logging.getLogger(__name__)
import sys

from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

import telnetlib


class TelnetClientException(CluAgentException):
  """
  Exceptions raised by TelnetClient
  """
  pass

class TelnetClient(Configurable):
  """
  Telnet client handler
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults = {"host":"localhost", "port":23}
    self.__defaults__(defaults)
    self.client = telnetlib.Telnet()

  def connect(self):
    """ Connect the client """
    try:
      self.client.open(self.config.host, self.config.port)
    except Exception, ex:
      LOGGER.error("Error connecting telnet client")
      raise TelnetClientException, TelnetClientException(ex), sys.exc_info()[2] # keep stacktrace

  def disconnect(self):
    """ Disconnect the client """
    try:
      self.client.close()
    except Exception, ex:
      LOGGER.error("Error disconnecting telnet client")
      raise TelnetClientException, TelnetClientException(ex), sys.exc_info()[2] # keep stacktrace
