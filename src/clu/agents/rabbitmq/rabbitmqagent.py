""" Module containing Rabbitmq logic """
from clu.agents import ConfigurableCluAgent
from clu.agents.rabbitmq.rabbitmqclient import RabbitmqClient

import json

class RabbitMqAgent(ConfigurableCluAgent):
  """
  Rabbitmq agent
  """
  def __init__(self, config, rmqconf):
    ConfigurableCluAgent.__init__(self, config)
    defaults = {"channel":
        {"exchange":"", "type":""},
        "messages":{"routing_key":""}
        }
    self.__defaults__(defaults)
    self.rmq = RabbitmqClient(rmqconf)

  def before_execute(self):
    try:
      ConfigurableCluAgent.before_execute(self)
    finally:
      self.rmq.connect()
      channel = self.rmqchannel()
      channel.exchange_declare(exchange=self.config.channel.exchange,
        type=self.config.channel.type)
      #

  def ensure_after_execute(self):
    try:
      ConfigurableCluAgent.ensure_after_execute(self)
    finally:
      self.rmq.disconnect()

  def rmqchannel(self):
    """
    Return the rmq channel
    """
    return self.rmq.channel

  def basic_publish(self, objmessage):
    """
    Publish on the rmq channel
    """
    message = json.dumps(objmessage)
    channel = self.rmqchannel()
    channel.basic_publish(exchange=self.config.channel.exchange,
        routing_key=self.config.messages.routing_key,
        body=message)
    #
