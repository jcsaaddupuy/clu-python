#!/usr/bin/env python2
import unittest
from mock import Mock, patch, mock_open
from clu.common.config.configurator import Configurator, ConfiguratorException

import os

class ConfiguratorTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    """ Test Configurator with empty params """
    co = Configurator({})
    self.assertTrue(co.config.filename is None)
    self.assertTrue(co.config.folder is None)
  
  def test_init_filename_param(self):
    """ Test Configurator with some params """
    co = Configurator({"filename":"afile", "folder" : "afolder"})
    self.assertTrue(co.config.filename == "afile")
    self.assertTrue(co.config.folder == "afolder")
  
  def test_init_filename_none(self):
    """ Test Configurator with filename None """
    co = Configurator({"folder" : "afolder"})
    with self.assertRaisesRegexp(ConfiguratorException, "Config file is not defined"):
      co.loadfile()
  
  def test_init_folder_none(self):
    """ Test Configurator with filename None """
    co = Configurator({"filename" : "afile"})
    with self.assertRaisesRegexp(ConfiguratorException, "Config folder is not defined"):
      co.loadfile()

  @patch.object(os.path,'exists')
  def test_init_file_does_not_exists(self, mocked):
    """ Test Configurator with non existing file """
    # Mock os.path.exists == False
    mocked.return_value = False

    co = Configurator({"filename":"afile", "folder" : "afolder"})
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
      co = Configurator({"filename":"afile", "folder" : "afolder"})
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
      co = Configurator({"filename":"afile", "folder" : "afolder"})
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
      co = Configurator({"filename":"afile", "folder" : "afolder"})
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


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(ConfiguratorTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
