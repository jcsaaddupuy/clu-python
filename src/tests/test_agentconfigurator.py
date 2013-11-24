#!/usr/bin/env python2
import unittest
from mock import Mock, patch, mock_open
from clu.common.config.agentconfigurator import AgentConfigurator, AgentConfiguratorException

import os

class AgentConfiguratorTestCase(unittest.TestCase):
  

  def test_loadclasses_config_not_loaded(self):
    """ Test AgentConfigurator with non existing file """
    co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
    with self.assertRaisesRegexp(AgentConfiguratorException, "not loaded"):
      co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agents(self, exists_mocked):
    """ Test AgentConfigurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agas":[{"name":"mpdstatus", "classname":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      with self.assertRaisesRegexp(AgentConfiguratorException, "Could not find agents in json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agent_name(self, exists_mocked):
    """ Test AgentConfigurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"nam":"mpdstatus", "classname":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      with self.assertRaisesRegexp(AgentConfiguratorException, "Could not find agent name in json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agent_class(self, exists_mocked):
    """ Test AgentConfigurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "clazz":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      with self.assertRaisesRegexp(AgentConfiguratorException, "Could not find agent classname json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_is_not_a_class(self, exists_mocked):
    """ Test AgentConfigurator with a module as classname"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      with self.assertRaisesRegexp(AgentConfiguratorException, "is not a type"):
        co.loadclasses()

  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_ok(self, exists_mocked):
    """ Test AgentConfigurator with a module as classname"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      co.loadclasses()

      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(co.__clazzs__["mpdstatus"]== MpdRmqAgent)
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_noconf(self, exists_mocked):
    """ Test AgentConfigurator with a full valid classname and no conf at all"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      co.loadclasses()
      co.initalize_all()

      self.assertTrue(len(co.agents) == 1)
      
      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(type(co.agents[0]) == MpdRmqAgent)
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_confempty(self, exists_mocked):
    """ Test AgentConfigurator with a full valid classname and an empty conf"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}],"configs":{}}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      co.loadclasses()
      co.initalize_all()

      self.assertTrue(len(co.agents) == 1)
      
      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(type(co.agents[0]) == MpdRmqAgent)
  
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_withconf(self, exists_mocked):
    """ Test AgentConfigurator agent instanciation with a full valid classname and configuration"""
    # Mock os.path.exists == True
    import json
    exists_mocked.return_value = True
    
    conf={"channel":{"exchange":"home.events","type":"topic"},"messages":{"routing_key":"home.events.multimedia.music.mpd"}}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    
    agentconfstr = json.dumps(conf)
    mpdconfstr = json.dumps(mpdconf)
    rmqconfstr = json.dumps(rmqconf)
    agentconf='{"config":%s, "mpdconf": %s, "rmqconf":%s}'%(agentconfstr, mpdconfstr, rmqconfstr)
    full_conf = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}],"configs":{"mpdstatus":%s}}'%(agentconf)
    m = mock_open(read_data = full_conf)

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = AgentConfigurator({"filename":"afile", "folder" : "afolder"})
      co.loadfile()
      co.loadclasses()
      co.initalize_all()

      self.assertTrue(len(co.agents) == 1)
      
      from clu.agents.mpd.mpdagent import MpdRmqAgent
      instance = co.agents[0]
      self.assertTrue(type(instance) == MpdRmqAgent)
      self.assertTrue(instance.config is not None)
      self.assertTrue(instance.config.channel.exchange == "home.events")
      self.assertTrue(instance.config.channel.type == "topic")
      
      self.assertTrue(instance.config.messages.routing_key == "home.events.multimedia.music.mpd")
      
      self.assertTrue(instance.mpdclient is not None)
      self.assertTrue(instance.mpdclient.config.host == "mpd.lan")
      
      self.assertTrue(instance.rmq is not None)
      self.assertTrue(instance.rmq.config.host == "rmq.lan")

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(AgentConfiguratorTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
