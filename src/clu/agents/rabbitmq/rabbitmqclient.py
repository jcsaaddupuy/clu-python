""" Module containg Rabbitmq client class """
import logging
LOGGER = logging.getLogger(__name__)
import sys

import pika

from clu.common.base import Configurable

class RabbitmqClientException(Exception):
  """ Exceptionss raised by RabbitmqClient """
  pass

class RabbitmqClient(Configurable):
  """
  Rabbitmq client handler.
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults = {
        "host":"localhost",
        "port":5672,
        "user":"guest",
        "password":"guest"
        }
    self.__defaults__(defaults)

    self.connection = None
    self.channel = None


  def connect(self):
    """Connection method """
    LOGGER.info("Connect Rabbitmq client")
    try:
      LOGGER.debug("Create Rabbitmq client Credentials")
      cred = pika.PlainCredentials(self.config.user, self.config.password)
      LOGGER.debug("Create Rabbitmq client Parameters")
      params =  pika.ConnectionParameters(
          host=str(self.config.host),
          port=self.config.port, credentials=cred
          )
      LOGGER.debug("Establishing Rabbitmq client connection")
      self.connection = pika.BlockingConnection(params)
      LOGGER.debug("Obtaining Rabbitmq client channel")
      self.channel = self.connection.channel()
    except Exception, ex:
      LOGGER.error("Error connecting (%s %s - %s %s)", type(self.config.host), self.config.host, type(self.config.port), self.config.port)
      raise RabbitmqClientException, RabbitmqClientException(ex), sys.exc_info()[2] # keep stacktrace

  def disconnect(self):
    """
    Disconnection method
    """
    try:
      if self.connection is not None:
        LOGGER.info("Closing Rabbitmq connection")
        if not (self.connection.is_closed or self.connection.is_closing):
          self.connection.close()
        else:
          LOGGER.info("RabbitMq Connection was already closed or was closing.")
      else:
        LOGGER.info("RabbitMq Connection was None, not closed")
    except Exception, ex:
      LOGGER.error("Error closing rabbitmq client connection")
      raise RabbitmqClientException, RabbitmqClientException(ex), sys.exc_info()[2] # keep stacktrace
