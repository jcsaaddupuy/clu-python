#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgentException
from clu.agents.mpd.mpdagent import MusicPlayerDaemon, MusicPlayeraemonEception
from mpd import ConnectionError, CommandError, MPDError

class MpdAgentTestCase(unittest.TestCase):

  def test_mpdagent_init_empty_params(self):
    mpdagent = MusicPlayerDaemon()
    self.assertTrue(mpdagent.config.host == "localhost")
    self.assertTrue(mpdagent.config.port == 6600)
    self.assertTrue(mpdagent.config.password is None)
  
  def test_mpdagent_init_with_mpd_conf(self):
    mpdconf={"host":"host","port":6601}
    mpdagent = MusicPlayerDaemon(mpdconf)
    
    self.assertTrue(mpdagent.config.host == "host")
    self.assertTrue(mpdagent.config.password is None)
    self.assertTrue(mpdagent.config.port == 6601)
    
    self.assertTrue(mpdagent.mpd is not None)
  
  def test_mpdagent_connect_no_password(self):
    mpdconf={"host":"host","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
  
  def test_mpdagent_connect_password(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdagent = MusicPlayerDaemon(mpdconf)

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
    mpdagent = MusicPlayerDaemon(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method
    connect=Mock(side_effect=ConnectionError())
    mpdmock.connect=connect
    
    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()
  
  
  def test_mpdagent_disconnect_mpdexception_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method
    disconnect=Mock(side_effect=MPDError())
    mpdmock.disconnect=disconnect
    
    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.disconnect()

  
  def test_mpdagent_connect_bad_password_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600, "password":"bad_pass"}
    mpdagent = MusicPlayerDaemon(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the password method
    password=Mock(side_effect=CommandError())
    mpdmock.password=password
    
    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()
      
    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])
  
  def test_mpdagent_connectexception_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)
    
    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method and reaise MPDError
    connect=Mock(side_effect=MPDError())
    mpdmock.connect=connect
    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()
      
    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])

from clu.agents.mpd.mpdagent import MpdRmqAgent
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mock import patch
class MpdRmqAgentTestCase(unittest.TestCase):
  def test_mpdrmq_agent_init(self):
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)
    self.assertFalse(agent.mpdagent is None)
    self.assertTrue(agent.mpdagent.config.host == "mpd.lan")
    self.assertFalse(agent.mpdagent.mpd is None)
    
    self.assertFalse(agent.rmqagent is None)
    self.assertTrue(agent.rmqagent.config.host == "rmq.lan")
  
  def test_mpdrmq_agent_run_call_connect(self):
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    mpdmock=Mock()
    agent.mpdagent=mpdmock

    rmqmock=Mock()
    agent.rmqagent=rmqmock
    # Mock the execute method to get rid of Not implemented exceptions
    execute=Mock()
    agent.execute=execute
    agent.run()

    mpdmock.connect.assert_called()
    mpdmock.connect.assert_called()
    rmqmock.disconnect.assert_called()
    rmqmock.disconnect.assert_called()

  @patch.object(RabbitMqAgent, 'before_execute')
  def test_mpdrmq_before_execute(self, mocked):
    """ Test that the call to before_execute call superclass before_execute"""
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    #Setup generic mock for others methos wich are not tested here
    ignoredmocks=Mock()
    agent.mpdagent=ignoredmocks
    agent.rmqagent=ignoredmocks
    

    instance = mocked.return_value 
    agent.before_execute()
    mocked.assert_called_with(agent)

  
  @patch.object(RabbitMqAgent, 'after_execute')
  def test_mpdrmq_after_execute(self, mocked):
    """ Test that the call to after_execute call superclass after_execute"""
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.mpdagent=ignoredmocks
    agent.rmqagent=ignoredmocks
    

    instance = mocked.return_value 
    agent.after_execute()
    mocked.assert_called_with(agent)

    


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentTestCase))
  suite.addTest(loader.loadTestsFromTestCase(MpdRmqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
