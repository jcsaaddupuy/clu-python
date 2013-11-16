#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.rabbitmq.common.base import WhiteRabbit, RabbitAgent


class WhiteRabbitTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = WhiteRabbit()
  
  def test_init_host_param(self):
    config={"host":"host"}
    co = WhiteRabbit(config)
    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "guest")
    self.assertTrue(co.config.password == "guest")
    self.assertTrue(co.config.port == 5672)

  def test_init_host_password_param(self):
    config={"host":"host", "password":"password", "port":56722}
    co = WhiteRabbit(config)

    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "guest")
    self.assertTrue(co.config.password == "password")
    self.assertTrue(co.config.port == 56722)


  
  def test_getchannel(self):
    config={"host":"host", "password":"password"}
    co = WhiteRabbit(config)

    #Mock the connection
    _conn = Mock()
    co._connection = _conn
    
    chan = co.channel()
    chan = co.channel()
    
    _conn.assert_called_once()

  def test_init_with_rabbit(self):
    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitAgent(config)
    self.assertFalse(co.rabbit is None)
    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "user")
    self.assertTrue(co.config.password == "password")
    self.assertTrue(co.config.port == 5656)



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(WhiteRabbitTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
