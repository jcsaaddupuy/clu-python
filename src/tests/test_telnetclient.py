import unittest
from mock import Mock, MagicMock, patch

from clu.agents import CluAgentException
from clu.agents.telnet.telnetclient import TelnetClient, TelnetClientException

import telnetlib

class TelnetClientAgentTestCase(unittest.TestCase):

  def test_telnetclient_init_empty_params(self):
    """ Test default config """
    telnetclient = TelnetClient()
    self.assertTrue(telnetclient.config.host == "localhost")
    self.assertTrue(telnetclient.config.port == 23)
    

  def test_telnetclient_init_with_telnetclient_conf(self):
    """ Test config """
    telnetclientconf={"host":"host","port":20000}
    telnetclient = TelnetClient(telnetclientconf)
    self.assertTrue(telnetclient.config.host == "host")
    self.assertTrue(telnetclient.config.port == 20000)

  @patch.object(telnetlib, 'Telnet')
  def test_telnetclient_connect(self, mocked):
    """ Test connect() method """
    telnetclientconf={"host":"host","port":20000}
    telnetclient = TelnetClient(telnetclientconf)

    telnetclient.connect()
    mocked.assert_called_with()
    telnetclient.client.open.assert_called_with(telnetclientconf["host"], telnetclientconf["port"])
  
  @patch.object(telnetlib.Telnet, 'open')
  def test_telnetclient_connect_exception(self, mocked):
    """ Test connect() method with exception raised """
    mocked.side_effect=Exception("In your face")

    telnetclientconf={"host":"host","port":20000}
    telnetclient = TelnetClient(telnetclientconf)

    with self.assertRaises(TelnetClientException):
      telnetclient.connect()
  
  @patch.object(telnetlib.Telnet, 'close')
  def test_telnetclient_disconnect_exception(self, mocked):
    """ Test disconnect() method with exception raised """
    mocked.side_effect=Exception("In your face !")

    telnetclientconf={"host":"host","port":20000}
    telnetclient = TelnetClient(telnetclientconf)

    with self.assertRaises(TelnetClientException):
      telnetclient.disconnect()
  
  @patch.object(telnetlib, 'Telnet')
  def test_telnetclient_disconnect(self, mocked):
    """ Test disconnect() method """
    telnetclientconf={"host":"host","port":20000}
    telnetclient = TelnetClient(telnetclientconf)

    # Call
    telnetclient.connect()
    telnetclient.disconnect()
    telnetclient.client.close.assert_called_with()



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(TelnetClientAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
