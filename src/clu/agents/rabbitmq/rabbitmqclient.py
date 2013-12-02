""" Module containg Rabbitmq client class """
import logging
LOGGER = logging.getLogger(__name__)
import sys

import pika

from clu.common.base import Configurable
import json

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

    self._connection = None
    self._channel = None

  def is_connection_valid(self):
    return self._connection is not None and not self._connection.is_closed and not self._connection.is_closing

  def is_channel_valid(self):
    return self._channel is not None and not self._channel.is_closed and not self._channel.is_closing



  def connect(self):
    """Connection method """
    if not self.is_connection_valid():
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
        self._connection = pika.BlockingConnection(params)
        LOGGER.debug("Obtaining Rabbitmq client channel")
      except Exception, ex:
        LOGGER.error("Error connecting (%s %s - %s %s)", type(self.config.host), self.config.host, type(self.config.port), self.config.port)
        raise RabbitmqClientException, RabbitmqClientException(ex), sys.exc_info()[2] # keep stacktrace
    else:
      LOGGER.info("Reusing Rabbitmq connection")
    
    if not self.is_channel_valid():
      LOGGER.info("Obtaining channel")
      self._channel = self._connection.channel()
    else:
      LOGGER.info("Reusing Rabbitmq channel")


  def disconnect(self):
    """
    Disconnection method
    """
    try:
      if self.is_connection_valid():
        LOGGER.info("Closing Rabbitmq connection")
        self._connection.close()
        self._connection = None
        self._channel = None
      else:
        LOGGER.info("RabbitMq Connection was already closed or was closing.")
    except Exception, ex:
      LOGGER.error("Error closing rabbitmq client connection")
      raise RabbitmqClientException, RabbitmqClientException(ex), sys.exc_info()[2] # keep stacktrace
    
    
  def ensure_valid_connection_channel(self):
    if not self.is_channel_valid():
      LOGGER.error("Trying to publish on a non valid channel, creating one")
      self.connect()
      if not self.is_connection_valid():
        raise RabbitmqClientException("Could not get valid connection")
      if not self.is_channel_valid():
        raise RabbitmqClientException("Could not get valid channel")
  
  def basic_publish(self, exchange, type, routing_key, message):
    """
    Publish on the rmq channel
    """
    self.ensure_valid_connection_channel()
    self._channel.exchange_declare(exchange=exchange,type=type)
    self._channel.basic_publish(exchange=exchange,
        routing_key=routing_key,
        body=message)
    #
  def basic_publish_json(self, exchange, type, routing_key, objmessage):
    message = json.dumps(objmessage)
    self.basic_publish(exchange, type,  routing_key, message)
