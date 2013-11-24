#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock, patch

from clu.common.base import AutoConfigurableException
from clu.agents.base import ConfigurableCluAgent

from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent



class RabbitMqAgentTestCase(unittest.TestCase):

  def test_rabbitmqagent_init_empty_params(self):
    rmqagent = RabbitMqAgent({},{})
    self.assertFalse(rmqagent.config.channel is None)
    self.assertTrue(rmqagent.config.channel.type == "")
    self.assertTrue(rmqagent.config.channel.exchange == "")
    
    self.assertFalse(rmqagent.config.messages is None)
    self.assertTrue(rmqagent.config.messages.routing_key == "")
    
    self.assertFalse(rmqagent.rmq is None)
  
  def test_rabbitmqagent_config(self):
    conf={"channel":{"exchange":"ex","type":"type"},"messages":{"routing_key":"rt"}}
    rmqagent = RabbitMqAgent(conf, {})
    self.assertFalse(rmqagent.config.channel is None)
    self.assertTrue(rmqagent.config.channel.type == "type")
    self.assertTrue(rmqagent.config.channel.exchange == "ex")
    
    self.assertFalse(rmqagent.config.messages is None)
    self.assertTrue(rmqagent.config.messages.routing_key == "rt")

  def test_rabbitmqagent_before_execute(self):
    conf={"channel":{"exchange":"ex","type":"type"}}
    rmqagent = RabbitMqAgent({},{})

    rmq = Mock()
    rmqagent.rmq = rmq

    rmqagent.before_execute()

    rmq.connect.assert_called_once_with()
    rmq.channel.exchange_declare(exchange=conf["channel"]["exchange"], type=conf["channel"]["type"])

  
  def test_rabbitmqagent_ensure_after_execute(self):
    rmqagent = RabbitMqAgent({},{})

    rmq = Mock()
    rmqagent.rmq = rmq

    rmqagent.ensure_after_execute()

    rmq.disconnect.assert_called_once_with()
  
  @patch.object(ConfigurableCluAgent,'before_execute')
  def test_rabbitmqagent_before_execute_call_super(self, method):
    rmqagent = RabbitMqAgent({},{})

    rmq = Mock()
    rmqagent.rmq = rmq

    rmqagent.before_execute()

    method.assert_called_once_with(rmqagent)
  
  
  @patch.object(ConfigurableCluAgent,'ensure_after_execute')
  def test_rabbitmqagent_ensure_after_execute_call_super(self, method):
    rmqagent = RabbitMqAgent({},{})

    rmq = Mock()
    rmqagent.rmq = rmq

    rmqagent.ensure_after_execute()

    method.assert_called_once_with(rmqagent)

  def test_rabbitmqagent_basicpublish(self):
    import json
    conf={"channel":{"exchange":"ex","type":"type"},"messages":{"routing_key":"rt"}}
    rmqagent = RabbitMqAgent(conf, {})

    rmq = Mock()
    rmqagent.rmq = rmq
    
    obj={"aa":1, "bb":{"cc":2}}
    rmqagent.basic_publish(obj)

    message=json.dumps(obj)
    rmq.channel.basic_publish.assert_called_once_with(exchange=conf["channel"]["exchange"], routing_key=conf["messages"]["routing_key"], body=message)


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(RabbitMqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
