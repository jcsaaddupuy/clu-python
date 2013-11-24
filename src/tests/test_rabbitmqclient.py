#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock, patch

from clu.common.base import AutoConfigurableException

from clu.agents.rabbitmq.rabbitmqclient import RabbitmqClient, RabbitmqClientException

class RabbitmqClientTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = RabbitmqClient()
  
  def test_init_host_param(self):
    config={"host":"host"}
    co = RabbitmqClient(config)
    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "guest")
    self.assertTrue(co.config.password == "guest")
    self.assertTrue(co.config.port == 5672)

  def test_init_host_password_param(self):
    config={"host":"host", "password":"password", "port":56722}
    co = RabbitmqClient(config)

    self.assertTrue(co.config.host == "host")
    self.assertTrue(co.config.user == "guest")
    self.assertTrue(co.config.password == "password")
    self.assertTrue(co.config.port == 56722)



  def test_connect(self):
    credpatcher = patch('pika.PlainCredentials')
    mockedcred = credpatcher.start()
    
    paramspatcher = patch('pika.ConnectionParameters')
    mockedparams = paramspatcher.start()
    
    conpatcher = patch('pika.BlockingConnection')
    mockedcon = conpatcher.start()
    
    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitmqClient(config)

    co.connect()
    self.assertFalse(co.channel is None)


    mockedcred.assert_called_with(config["user"], config["password"])
    mockedparams.assert_called_with(host=config["host"], port=config["port"], credentials=mockedcred.return_value)
    mockedcon.assert_called_with(mockedparams.return_value)

    credpatcher.stop()
    paramspatcher.stop()
    conpatcher.stop()
  
  def test_connect_exceptions(self):
    credpatcher = patch('pika.PlainCredentials')
    mockedcred = credpatcher.start()
    
    paramspatcher = patch('pika.ConnectionParameters')
    mockedparams = paramspatcher.start()
    
    conpatcher = patch('pika.BlockingConnection')
    mockedcon = conpatcher.start()
    mockedcon.side_effect=Exception("In your face")
    
    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitmqClient(config)
    
    with self.assertRaises(RabbitmqClientException):
      co.connect()

    credpatcher.stop()
    paramspatcher.stop()
    conpatcher.stop()

  def test_disconnect(self):
    conn = Mock()
    close = Mock()

    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitmqClient(config)
    co.connection=conn
    conn.close=close

    co.disconnect()
    close.assert_called()
  
  def test_disconnect_exception(self):
    conn = Mock()
    close = Mock()
    close.side_effect=Exception("In your face")

    config={"host":"host", "port":5656, "user":"user","password":"password"}
    co = RabbitmqClient(config)
    co.connection=conn
    conn.close=close

    with self.assertRaises(RabbitmqClientException):
      co.disconnect()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(RabbitmqClientTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
