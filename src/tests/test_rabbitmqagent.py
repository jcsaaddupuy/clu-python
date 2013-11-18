#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock, patch

from clu.common.base import AutoConfigurableException
from clu.agents.base import ConfigurableCluAgent

from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent



class RabbitMqAgentTestCase(unittest.TestCase):

  def test_rabbitmqagent_init_empty_params(self):
    rmq = RabbitMqAgent()
    self.assertFalse(rmq.config.channel is None)
    self.assertTrue(rmq.config.channel.type == "")
    self.assertTrue(rmq.config.channel.exchange == "")
    
    self.assertFalse(rmq.config.messages is None)
    self.assertTrue(rmq.config.messages.routing_key == "")
    
    self.assertFalse(rmq.rmqagent is None)
  
  def test_rabbitmqagent_config(self):
    conf={"channel":{"exchange":"ex","type":"type"},"messages":{"routing_key":"rt"}}
    rmq = RabbitMqAgent(conf)
    self.assertFalse(rmq.config.channel is None)
    self.assertTrue(rmq.config.channel.type == "type")
    self.assertTrue(rmq.config.channel.exchange == "ex")
    
    self.assertFalse(rmq.config.messages is None)
    self.assertTrue(rmq.config.messages.routing_key == "rt")

  def test_rabbitmqagent_before_execute(self):
    conf={"channel":{"exchange":"ex","type":"type"}}
    rmq = RabbitMqAgent()

    rmqagent = Mock()
    rmq.rmqagent = rmqagent

    rmq.before_execute()

    rmqagent.connect.assert_called_once_with()
    rmqagent.channel.exchange_declare(exchange=conf["channel"]["exchange"], type=conf["channel"]["type"])

  
  def test_rabbitmqagent_ensure_after_execute(self):
    rmq = RabbitMqAgent()

    rmqagent = Mock()
    rmq.rmqagent = rmqagent

    rmq.ensure_after_execute()

    rmqagent.disconnect.assert_called_once_with()
  
  @patch.object(ConfigurableCluAgent,'before_execute')
  def test_rabbitmqagent_before_execute_call_super(self, method):
    rmq = RabbitMqAgent()

    rmqagent = Mock()
    rmq.rmqagent = rmqagent

    rmq.before_execute()

    method.assert_called_once_with(rmq)
  
  @patch.object(ConfigurableCluAgent,'after_execute')
  def test_rabbitmqagent_before_execute_call_super(self, method):
    rmq = RabbitMqAgent()

    rmqagent = Mock()
    rmq.rmqagent = rmqagent

    rmq.after_execute()

    method.assert_called_once_with(rmq)
  
  @patch.object(ConfigurableCluAgent,'ensure_after_execute')
  def test_rabbitmqagent_ensure_after_execute_call_super(self, method):
    rmq = RabbitMqAgent()

    rmqagent = Mock()
    rmq.rmqagent = rmqagent

    rmq.ensure_after_execute()

    method.assert_called_once_with(rmq)

  def test_rabbitmqagent_basicpublish(self):
    import json
    conf={"channel":{"exchange":"ex","type":"type"},"messages":{"routing_key":"rt"}}
    rmq = RabbitMqAgent(conf)

    rmqagent = Mock()
    rmq.rmqagent = rmqagent
    
    obj={"aa":1, "bb":{"cc":2}}
    rmq.basic_publish(obj)

    message=json.dumps(obj)
    rmqagent.channel.basic_publish.assert_called_once_with(exchange=conf["channel"]["exchange"], routing_key=conf["messages"]["routing_key"], body=message)


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(RabbitMqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
