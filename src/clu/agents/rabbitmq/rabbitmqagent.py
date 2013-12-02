""" Module containing Rabbitmq logic """
from clu.agents import ConfigurableCluAgent
from clu.agents.rabbitmq.rabbitmqclient import RabbitmqClient


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
    self.rmqclient = RabbitmqClient(rmqconf)


  def ensure_after_execute(self):
    try:
      ConfigurableCluAgent.ensure_after_execute(self)
    finally:
      self.rmqclient.disconnect()

  def basic_publish_json(self, message):
    real_message = {}
    real_message["id"] = self.id
    real_message["payload"] = message
    self.rmqclient.basic_publish_json(self.config.channel.exchange, self.config.channel.type, self.config.messages.routing_key, real_message)
