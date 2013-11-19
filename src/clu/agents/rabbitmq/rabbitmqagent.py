from clu.agents import ConfigurableCluAgent, CluAgentException
from rabbitmqclient import RabbitmqClient

import json
class RabbitMqAgent(ConfigurableCluAgent):
  """
  Rabbitmq agent
  """
  def __init__(self, config={}, rmqconf={}):
    ConfigurableCluAgent.__init__(self, config)
    defaults={"channel":{"exchange":"","type":""},"messages":{"routing_key":""}}
    self.__defaults__(defaults)
    self.rmqagent=RabbitmqClient(rmqconf)
    
    
  def before_execute(self):
    try:
      ConfigurableCluAgent.before_execute(self)
    finally:
      self.rmqagent.connect()
      channel = self.rmqchannel()
      channel.exchange_declare(exchange=self.config.channel.exchange, type=self.config.channel.type)

  def ensure_after_execute(self):
    try:
      ConfigurableCluAgent.ensure_after_execute(self)
    finally:
      self.rmqagent.disconnect()
  
  def rmqchannel(self):
    return self.rmqagent.channel

  def basic_publish(self, objmessage):
    message=json.dumps(objmessage)
    channel = self.rmqchannel()
    channel.basic_publish(exchange=self.config.channel.exchange, routing_key=self.config.messages.routing_key, body=message)
