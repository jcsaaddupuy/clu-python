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

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(ConfiguratorTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
