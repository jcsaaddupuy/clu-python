#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgent, ConfigurableCluAgent, CluException, CluAgentException

class CluAgentTestCase(unittest.TestCase):
  def test_cluagent_execute_raises_cluagentexception(self):
    cluagent = CluAgent()
    with self.assertRaises(CluException):
      cluagent.run()
  
  def test_cluagent_call_before_execute(self):
    cluagent = CluAgent()
    before_execute=Mock()
    cluagent.before_execute=before_execute
    with self.assertRaises(CluException):
      cluagent.run()
    before_execute.assert_called_once_with()
  
  def test_cluagent_call_before_execute_excption(self):
    cluagent = CluAgent()
    before_execute=Mock(side_effect=CluAgentException())
    cluagent.before_execute=before_execute
    
    with self.assertRaises(CluException):
      cluagent.run()
    
    before_execute.assert_called_once_with()
  
  def test_cluagent_call_before_rexecute_after(self):
    cluagent = CluAgent()
    before_execute=Mock()
    after_execute=Mock()
    execute=Mock()

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    
    cluagent.run()
    
    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()
  

class ConfigurableCluAgentTestCase(unittest.TestCase):
  def test_configcluagent_execute_raises_cluagentexception(self):
    cluagent = ConfigurableCluAgent()
    with self.assertRaises(CluException):
      cluagent.run()
  
  def test_configcluagent_call_before_execute(self):
    cluagent = ConfigurableCluAgent()
    before_execute=Mock()
    cluagent.before_execute=before_execute
    with self.assertRaises(CluException):
      cluagent.run()
    before_execute.assert_called_once_with()
  
  def test_configcluagent_call_before_execute_excption(self):
    cluagent = ConfigurableCluAgent()
    before_execute=Mock(side_effect=CluAgentException())
    cluagent.before_execute=before_execute
    
    with self.assertRaises(CluException):
      cluagent.run()
    
    before_execute.assert_called_once_with()
  
  def test_configcluagent_call_before_rexecute_after(self):
    cluagent = ConfigurableCluAgent()
    before_execute=Mock()
    after_execute=Mock()
    execute=Mock()

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    
    cluagent.run()
    
    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(CluAgentTestCase))
  suite.addTest(loader.loadTestsFromTestCase(ConfigurableCluAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestexecutener(verbosity=2).execute(suite())
