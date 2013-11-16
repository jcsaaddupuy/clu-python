#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgent, ConfigurableCluAgent, CluException

class CluAgentTestCase(unittest.TestCase):
  def test_mpdagent_run_raises_mpdagentexception(self):
    cluagent = CluAgent()
    with self.assertRaises(CluException):
      cluagent.run()

class ConfigurableCluAgentTestCase(unittest.TestCase):
  def test_mpdagent_run_raises_mpdagentexception(self):
    cluagent = ConfigurableCluAgent()
    with self.assertRaises(CluException):
      cluagent.run()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(CluAgentTestCase))
  suite.addTest(loader.loadTestsFromTestCase(ConfigurableCluAgent))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
