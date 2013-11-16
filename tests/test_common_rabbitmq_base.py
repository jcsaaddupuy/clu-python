#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock, patch

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


  def test_init_with_rabbit(self):
    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitAgent(config)
    self.assertFalse(co.rabbit is None)
    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "user")
    self.assertTrue(co.config.password == "password")
    self.assertTrue(co.config.port == 5656)

  def test_connect(self):
    credpatcher = patch('pika.PlainCredentials')
    mockedcred = credpatcher.start()
    
    paramspatcher = patch('pika.ConnectionParameters')
    mockedparams = paramspatcher.start()
    
    conpatcher = patch('pika.BlockingConnection')
    mockedcon = conpatcher.start()
    
    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = WhiteRabbit(config)

    co.connect()
    self.assertFalse(co.channel is None)


    mockedcred.assert_called_with(config["user"], config["password"])
    mockedparams.assert_called_with(host=config["host"], port=config["port"], credentials=mockedcred.return_value)
    mockedcon.assert_called_with(mockedparams.return_value)

    credpatcher.stop()
    paramspatcher.stop()
    conpatcher.stop()

  def test_disconnect(self):
    conn = Mock()
    close = Mock()

    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = WhiteRabbit(config)
    co.connection=conn
    conn.close=close

    co.disconnect()
    close.assert_called()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(WhiteRabbitTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
