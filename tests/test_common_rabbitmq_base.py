#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.rabbitmq.common.base import WhiteRabbit, RabbitAgent


class WhiteRabbitTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = WhiteRabbit()
  
  def test_init_host_param(self):
    co = WhiteRabbit(host="host")
    self.assertTrue(co.host == "host")
    self.assertTrue(co.password is None)
    self.assertTrue(co.port is None)

  def test_init_host_password_param(self):
    co = WhiteRabbit(host="host", password="password")
    self.assertTrue(co.host == "host")
    self.assertTrue(co.password == "password")
    self.assertTrue(co.port is None)
  
  def test_getchannel(self):
    co = WhiteRabbit(host="host", password="password")

    #Mock the connection
    _conn = Mock()
    co._connection = _conn
    
    chan = co.channel()
    chan = co.channel()
    
    _conn.assert_called_once()

  def test_init_with_rabbit(self):
    co = RabbitAgent(rmq_host="host", rmq_password="password", rmq_port=5656)
    self.assertFalse(co.rabbit is None)
    self.assertTrue(co.rabbit.host == "host")
    self.assertTrue(co.rabbit.password == "password")
    self.assertTrue(co.rabbit.port == 5656)



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(WhiteRabbitTestCase))
  return suite


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
