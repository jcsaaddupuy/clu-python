#!/usr/bin/env python2
import unittest
from mock import Mock, patch, mock_open
from clu.common.runner.agentrunner import AgentRunner, AgentRunnerException, SCHEDULERS

import os

class AgentRunnerTestCase(unittest.TestCase):
  def test_init_noparams(self):
    """ Test AgentRunner with no parameters """
    co = AgentRunner()
    self.assertTrue(co.scheduler is None)
    self.assertTrue(co.instance is None)
  
  def test_init_params(self):
    """ Test AgentRunner with parameters """
    sched = {"scheduling":{"name": "SCHED"}}
    co = AgentRunner(Mock())
    self.assertFalse(co.instance is None)
  
  
  def test_init_scheduler_unknown_scheduler(self):
    """ Test AgentRunner with parameters """
    instance = Mock()
    instance.config.scheduling.name = "BAD SCHEDULER"

    co = AgentRunner(instance)
    with self.assertRaisesRegexp(AgentRunnerException, "Scheduling strategies not found"):
      co._init_scheduler()

  def test_init_scheduler_loop_scheduler(self):
    """ Test AgentRunner scheduler instanciation """

    instance = Mock()
    instance.config.scheduling.name = "loop"

    co = AgentRunner(instance)
    co._init_scheduler()
    self.assertTrue(co.scheduler.__class__ is SCHEDULERS["loop"])

  def test_init_scheduler_none_scheduler(self):
    """ Test AgentRunner scheduler instanciation """

    instance = Mock()
    instance.config.scheduling.name = None

    co = AgentRunner(instance)
    co._init_scheduler()
    self.assertTrue(co.scheduler.__class__ is SCHEDULERS[None])
  
  def test_start_no_scheduler(self):
    """ Test AgentRunner with parameters """
    instance = Mock()
    mock = Mock()
    instance.config.scheduling.name = "A SCHEDULER"

    co = AgentRunner(instance)
    co._init_scheduler = mock

    with self.assertRaisesRegexp(AgentRunnerException, "No scheduler found"):
      co.start()
  
  def test_start_a_scheduler(self):
    """ Test AgentRunner with parameters """
    sched = {"scheduling":{"name": "A SCHEDULER"}}
    mock = Mock()
    mocked_sched = Mock()
    instance = Mock()

    co = AgentRunner(instance)
    co._init_scheduler = mock
    co.scheduler = mocked_sched

    co.start()
    mocked_sched.start.assert_called_with()
  
  def test_stop_no_scheduler(self):
    """ Test AgentRunner with parameters """
    sched = {"scheduling":{"name": "A SCHEDULER"}}
    instance = Mock()
    mock = Mock()

    co = AgentRunner(instance)
    co._init_scheduler = mock

    with self.assertRaisesRegexp(AgentRunnerException, "No scheduler found"):
      co.stop()
  
  def test_start_no_instance(self):
    """ Test AgentRunner with parameters """
    sched = {"scheduling":{"name": "A SCHEDULER"}}
    instance = None
    mock = Mock()

    co = AgentRunner(instance)

    with self.assertRaisesRegexp(AgentRunnerException, "Can't init a runner for a None module !"):
      co._init_scheduler()
  
  def test_stop_a_scheduler(self):
    """ Test AgentRunner with parameters """
    sched = {"scheduling":{"name": "A SCHEDULER"}}
    mock = Mock()
    mocked_sched = Mock()
    instance = Mock()

    co = AgentRunner(instance)
    co.scheduler = mocked_sched

    co.stop()
    mocked_sched.stop.assert_called_with()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(AgentRunnerTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
