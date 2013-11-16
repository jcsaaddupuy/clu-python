#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents.mpd.mpdagent import MpdAgent, MpdAgentException #,MpdControlAgent, MpdStatusAgent

from mpd import ConnectionError, CommandError

class MpdAgentsTestCase(unittest.TestCase):

  def test_mpdagent_init_empty_params(self):
    mpdagent = MpdAgent()
    self.assertTrue(mpdagent.config.host == "localhost")
    self.assertTrue(mpdagent.config.port == 6600)
    self.assertTrue(mpdagent.config.password is None)
  
  def test_mpdagent_init_with_mpd_conf(self):
    mpdconf={"host":"host","port":6601}
    mpdagent = MpdAgent(mpdconf)
    
    self.assertTrue(mpdagent.config.host == "host")
    self.assertTrue(mpdagent.config.password is None)
    self.assertTrue(mpdagent.config.port == 6601)
    
    self.assertTrue(mpdagent.mpd is not None)
  
  def test_mpdagent_connect_mpd_no_password(self):
    mpdconf={"host":"host","port":6600}
    mpdagent = MpdAgent(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect_mpd()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
  
  def test_mpdagent_connect_mpd_password(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdagent = MpdAgent(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect_mpd()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])
  
  def test_mpdagent_connect_bad_host_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MpdAgent(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method
    connect=Mock(side_effect=ConnectionError())
    mpdmock.connect=connect
    
    # Call
    with self.assertRaises(MpdAgentException):
      mpdagent.connect_mpd()
  
  def test_mpdagent_connect_bad_password_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600, "password":"bad_pass"}
    mpdagent = MpdAgent(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the password method
    password=Mock(side_effect=CommandError())
    mpdmock.password=password
    
    # Call
    with self.assertRaises(MpdAgentException):
      mpdagent.connect_mpd()
      
    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])

  def test_mpdagent_run_raises_mpdagentexception(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdagent = MpdAgent(mpdconf)
    with self.assertRaises(MpdAgentException):
      mpdagent.run()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentsTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
