#!/usr/bin/env python2
import unittest

from clu.agents.base import ConfigurableCluAgent


class ConfigurableCluAgentTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    co = ConfigurableCluAgent()
    self.assertTrue(co.config.name == "")
    self.assertTrue(co.name == "")
  
  def test_init_one_kwargs_param(self):
    co = ConfigurableCluAgent({"name":"myagent"})
    self.assertTrue(co.config.name == "myagent")
    self.assertTrue(co.name == "myagent")

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(ConfigurableCluAgentTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
