#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgent, ConfigurableCluAgent, CluException, CluAgentException

class CluAgentTestCase(unittest.TestCase):
  def test_cluagent_execute_raises_cluagentexception(self):
    """Ensure that the default method run raises an Exception"""
    cluagent = CluAgent()
    with self.assertRaises(CluException):
      cluagent.run()
  
  def test_cluagent_call_before_execute(self):
    """ Ensure that the method before_execute is called before execute() """
    cluagent = CluAgent()
    before_execute=Mock()
    cluagent.before_execute=before_execute
    with self.assertRaises(CluException):
      cluagent.run()
    before_execute.assert_called_once_with()
  
  def test_cluagent_call_before_execute_excption(self):
    """ Ensure that the method after_execute is called before execute() """
    cluagent = CluAgent()
    before_execute=Mock(side_effect=CluAgentException())
    cluagent.before_execute=before_execute
    
    with self.assertRaises(CluException):
      cluagent.run()
    
    before_execute.assert_called_once_with()
  
  def test_cluagent_call_before_execute_after(self):
    """ Ensure that all methods are called """
    cluagent = CluAgent()
    before_execute=Mock()
    after_execute=Mock()
    ensure_after_execute=Mock()
    execute=Mock()

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    cluagent.ensure_after_execute=ensure_after_execute
    
    cluagent.run()
    
    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()
    ensure_after_execute.assert_called_once_with()
  
  def test_cluagent_call_ensure_afterexecute_on_run_exception(self):
    """ Ensure that ensure_after_execute is called when execute() raise an Exception """
    cluagent = CluAgent()
    before_execute=Mock()
    after_execute=Mock()
    ensure_after_execute=Mock()
    execute=Mock(side_effect=Exception("In your face"))

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    cluagent.ensure_after_execute=ensure_after_execute
    
    with(self.assertRaises(CluAgentException)) as ex:
      cluagent.run()
    
    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    ensure_after_execute.assert_called_once_with()
  
  def test_cluagent_call_ensure_afterexecute_on_after_execute_exception(self):
    """ Ensure that ensure_after_execute is called when after_execute() raise an Exception """
    cluagent = CluAgent()
    before_execute=Mock()
    after_execute=Mock(side_effect=Exception("In you face"))
    ensure_after_execute=Mock()
    execute=Mock()

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    cluagent.ensure_after_execute=ensure_after_execute
    
    with(self.assertRaises(CluAgentException)) as ex:
      cluagent.run()
    
    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()
    ensure_after_execute.assert_called_once_with()

  def test_cluagent_call_ensure_execute_eception_raised_on_after_execute_exception(self):
    """ Ensure that when execute() and after_execute() raises an Exception, the first is raised"""
    ex_ensure_after=Exception("In your face")
    ex_after_execute=Exception("In your face su**cker")
    after_execute=Mock(side_effect=ex_after_execute)
    ensure_after_execute=Mock(side_effect=ex_ensure_after)
    
    cluagent = CluAgent()
    before_execute=Mock()
    execute=Mock()

    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    cluagent.ensure_after_execute=ensure_after_execute
    
    with(self.assertRaises(CluAgentException)) as e:
      cluagent.run()

    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()
    ensure_after_execute.assert_called_once_with()
  
  def test_cluagent_call_ensure_afterexecute_on_after_execute_exception_is_first(self):
    """ Ensure that when execute() and after_execute() raises an Exception, the first is raised"""
    ex_ensure_after=Exception("In your face")
    ensure_after_execute=Mock(side_effect=ex_ensure_after)
    
    cluagent = CluAgent()

    before_execute=Mock()
    execute=Mock()
    after_execute=Mock()
    
    cluagent.before_execute=before_execute
    cluagent.execute=execute
    cluagent.after_execute=after_execute
    cluagent.ensure_after_execute=ensure_after_execute
    
    with(self.assertRaises(CluAgentException)) as e:
      cluagent.run()

    before_execute.assert_called_once_with()
    execute.assert_called_once_with()
    after_execute.assert_called_once_with()
    ensure_after_execute.assert_called_once_with()


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(CluAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestexecutener(verbosity=2).execute(suite())
