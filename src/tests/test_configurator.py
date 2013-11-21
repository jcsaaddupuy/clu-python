#!/usr/bin/env python2
import unittest
from mock import Mock, patch, mock_open
from clu.common.config.configurator import Configurator, ConfiguratorException

import os

class ConfiguratorTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    """ Test Configurator with empty params """
    co = Configurator()
    self.assertTrue(co.config.filename is None)
  
  def test_init_filename_param(self):
    """ Test Configurator with some params """
    co = Configurator({"filename":"afile"})
    self.assertTrue(co.config.filename == "afile")
  
  def test_init_filename_none(self):
    """ Test Configurator with filename None """
    co = Configurator()
    with self.assertRaises(ConfiguratorException):
      co.loadfile()

  @patch.object(os.path,'exists')
  def test_init_file_does_not_exists(self, mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == False
    mocked.return_value = False

    co = Configurator({"filename":"afile"})
    with self.assertRaises(ConfiguratorException):
      co.loadfile()

  @patch.object(os.path,'exists')
  def test_init_file_bad_json(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = "BAD JSON}")

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      with self.assertRaises(ConfiguratorException):
        co.loadfile()
  
  @patch.object(os.path,'exists')
  def test_loadfile_ok(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"test":"Hello"}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      self.assertTrue(co._loadedconfig.has_key("test"))
  
  @patch.object(os.path,'exists')
  def test_loadfile_realconfig(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"", "type":""}], "configs":[{"name":"", "config":{}}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      self.assertTrue(co._loadedconfig.has_key("agents"))
      self.assertTrue(type(co._loadedconfig["agents"]) == list)
      
      for item in co._loadedconfig["agents"]:
        self.assertTrue(item.has_key("name"))
        self.assertTrue(item.has_key("type"))

      for item in co._loadedconfig["configs"]:
        self.assertTrue(item.has_key("name"))
        self.assertTrue(item.has_key("config"))
        self.assertTrue(type(item["config"]) == dict)

  def test_loadclasses_config_not_loaded(self):
    """ Test Configurator with non existing file """
    co = Configurator({"filename":"afile"})
    with self.assertRaisesRegexp(ConfiguratorException, "not loaded"):
      co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agents(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agas":[{"name":"mpdstatus", "classname":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      with self.assertRaisesRegexp(ConfiguratorException, "Could not find agents in json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agent_name(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"nam":"mpdstatus", "classname":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      with self.assertRaisesRegexp(ConfiguratorException, "Could not find agent name in json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_no_agent_class(self, exists_mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "clazz":""}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      with self.assertRaisesRegexp(ConfiguratorException, "Could not find agent classname json config"):
        co.loadclasses()
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_is_not_a_class(self, exists_mocked):
    """ Test Configurator with a module as classname"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      with self.assertRaisesRegexp(ConfiguratorException, "is not a type"):
        co.loadclasses()

  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_ok(self, exists_mocked):
    """ Test Configurator with a module as classname"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      co.loadclasses()

      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(co.__clazzs__["mpdstatus"]== MpdRmqAgent)
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_noconf(self, exists_mocked):
    """ Test Configurator with a full valid classname and no conf at all"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}]}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      co.loadclasses()
      co.initalize_all()

      self.assertTrue(len(co.agents) == 1)
      
      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(type(co.agents[0]) == MpdRmqAgent)
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_confempty(self, exists_mocked):
    """ Test Configurator with a full valid classname and an empty conf"""
    # Mock os.path.exists == True
    exists_mocked.return_value = True
    m = mock_open(read_data = '{"agents":[{"name":"mpdstatus", "classname":"clu.agents.mpd.mpdagent.MpdRmqAgent"}],"configs":{}}')

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
      co.loadfile()
      co.loadclasses()
      co.initalize_all()

      self.assertTrue(len(co.agents) == 1)
      
      from clu.agents.mpd.mpdagent import MpdRmqAgent
      self.assertTrue(type(co.agents[0]) == MpdRmqAgent)
  
  
  @patch.object(os.path,'exists')
  def test_loadclasses_config_agent_classname_withconf(self, exists_mocked):
    """ Test Configurator agent instanciation with a full valid classname and configuration"""
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
    print full_conf

    open_name = '%s.open' % "clu.common.config.configurator"
    with patch(open_name, m, create=True):
      co = Configurator({"filename":"afile"})
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
  suite.addTest(loader.loadTestsFromTestCase(ConfiguratorTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
