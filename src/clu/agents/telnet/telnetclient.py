#!/usr/bin/env python2
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
    defaults={"host":"localhost", "port":23}
    self.__defaults__(defaults)
    self.client = None

  def connect(self):
    """ Connect the client """
    try:
      # the constructor try to estalish a connection
      self.client = telnetlib.Telnet(self.config.host, self.config.port)
      self.client.open()
    except Exception, ex:
      raise TelnetClientException(ex)

  def disconnect(self):
    """ Disconnect the client """
    try:
      self.client.close()
    except Exception, e:
      raise TelnetClientException(e)
