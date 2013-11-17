#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgentException
from clu.agents.mpd.mpdagent import MpdAgent, MpdAgentException
from mpd import ConnectionError, CommandError, MPDError

class MpdAgentTestCase(unittest.TestCase):

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
  
  def test_mpdagent_connect_no_password(self):
    mpdconf={"host":"host","port":6600}
    mpdagent = MpdAgent(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
  
  def test_mpdagent_connect_password(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdagent = MpdAgent(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect()
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
      mpdagent.connect()
  
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
      mpdagent.connect()
      
    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])
  
  def test_mpdagent_connectexception_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MpdAgent(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method and reaise MPDError
    connect=Mock(side_effect=MPDError())
    mpdmock.connect=connect
    # Call
    with self.assertRaises(MpdAgentException):
      mpdagent.connect()
      
    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])

from clu.agents.mpd.mpdagent import MpdRmqAgent
class MpdRmqAgentTestCase(unittest.TestCase):
  def test_mpdrmq_statusagent_init(self):
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(mpdconf, rmqconf)
    self.assertFalse(agent.mpdagent is None)
    self.assertTrue(agent.mpdagent.config.host == "mpd.lan")
    
    self.assertFalse(agent.rmqagent is None)
    self.assertTrue(agent.rmqagent.config.host == "rmq.lan")
    
from clu.agents.mpd.mpdagent import MpdStatusAgent
class MpdStatusAgentTestCase(unittest.TestCase):
  def test_mpdrmq_statusagent_init(self):
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdStatusAgent(mpdconf, rmqconf)
    self.assertTrue(agent.mpdagent is not None)
    self.assertTrue(agent.mpdagent.config.host == "mpd.lan")
    
    self.assertTrue(agent.rmqagent is not None)
    self.assertTrue(agent.rmqagent.config.host == "rmq.lan")
  
  def test_mpdrmq_statusagent_run_readstatus(self):
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdStatusAgent(mpdconf, rmqconf)
    self.assertTrue(agent.mpdagent is not None)
    self.assertTrue(agent.mpdagent.config.host == "mpd.lan")
    
    self.assertTrue(agent.rmqagent is not None)
    self.assertTrue(agent.rmqagent.config.host == "rmq.lan")

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentTestCase))
  suite.addTest(loader.loadTestsFromTestCase(MpdRmqAgentTestCase))
  suite.addTest(loader.loadTestsFromTestCase(MpdStatusAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
