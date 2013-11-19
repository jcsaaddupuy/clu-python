#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgentException
from clu.agents.xbmc.xbmc import Xbmc

class XbmcAgentTestCase(unittest.TestCase):

  def test_xbmc_init_empty_params(self):
    xbmc = Xbmc()
    self.assertTrue(xbmc.config.host == "localhost")
    self.assertTrue(xbmc.config.port == 8080)
    self.assertTrue(xbmc.config.user == "xbmc")
    self.assertTrue(xbmc.config.password == "xbmc")
    
    self.assertTrue(xbmc.client is not None)

  def test_xbmc_init_with_xbmc_conf(self):
    xbmcconf={"host":"host","port":8081, "user":"USER", "password":"PASSWORD"}
    xbmc = Xbmc(xbmcconf)
    
    self.assertTrue(xbmc.config.host == "host")
    self.assertTrue(xbmc.config.port == 8081)
    self.assertTrue(xbmc.config.user == "USER")
    self.assertTrue(xbmc.config.password == "PASSWORD")


    self.assertTrue(xbmc.client is not None)

  def test_xbmc_getsonrpc(self):
    xbmcconf={}
    xbmc = Xbmc(xbmcconf)
    self.assertTrue(xbmc.get_json_rpc("host") == "host/jsonrpc")
    self.assertTrue(xbmc.get_json_rpc("host/") == "host/jsonrpc")



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(XbmcAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
