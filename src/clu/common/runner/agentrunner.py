""" Module containing agent runner """
import logging
LOGGER = logging.getLogger(__name__)
import sys

import threading

class NoneScheduler(object):
  """
  Default scheduler, just run once the agent
  """
  def __init__(self, instance = None):
    self.instance = instance

  def start(self):
    """ starts the agent """
    self.instance.run()

  def stop(self):
    """ Stop the agent """
    pass

class AgentRunnerException(Exception):
  """  Exception raised by ModuleRunner """
  pass

class LoopScheduler(threading.Thread):
  """
  Execute an agent inside a loop
  """
  def __init__(self, instance = None, wait = 0.001, wait_on_error = 5, max_retry = None):
    threading.Thread.__init__(self)
    self.wait = wait
    self.wait_on_error = wait_on_error
    self.instance = instance

    self._stopevent = threading.Event()
    self.max_retry = max_retry
    self.tryed = 0
    LOGGER.info("LoopScheduler initialized")

  def run(self):
    """ starts the agent """
    LOGGER.info("Starting LoopScheduler for '%s'", self.instance)

    while not self._stopevent.isSet() and not self.max_retry_reached():
      self.tryed += 1
      try:
        self.instance.run()
        self._stopevent.wait(self.wait)
      except Exception, ex:
        LOGGER.exception("Error while running agent (%s/%s).", self.tryed, "Unlimited" if self.max_retry is None else self.max_retry)
        self._stopevent.wait(self.wait_on_error)

  def stop(self):
    """ Stop the agent """
    LOGGER.info("Stoping LoopScheduler")
    self._stopevent.set()
    self._Thread__stop()

  def max_retry_reached(self):
    """ Return True if max errors reached """
    return self.max_retry is not None and self.tryed >= self.max_retry

SCHEDULERS = {
    None : NoneScheduler,
    "loop": LoopScheduler,
    }

class AgentRunner(object):
  """Class handling running agent"""
  def __init__(self, instance = None):
    self.instance = instance
    self.scheduler = None

  def _init_scheduler(self):
    """ Initialize the scheduler """
    if self.instance is None:
      raise AgentRunnerException("Can't init a runner for a None module !")

    if not SCHEDULERS.has_key(self.instance.config.scheduling.name):
      msg = "Scheduling strategies not found! Possibles values : %s" % (SCHEDULERS.keys())
      raise AgentRunnerException(msg)
    else:
      # Initialize the scheduler
      self.scheduler = SCHEDULERS[self.instance.config.scheduling.name](self.instance)


  def start(self):
    """
    Start the scheduler
    """
    self._init_scheduler()
    if self.scheduler is None:
      msg = "No scheduler found"
      raise AgentRunnerException(msg)

    LOGGER.info("Starting '%s' with '%s' scheduler", self.instance.name, self.scheduler.__class__)
    self.scheduler.start()
    return self.scheduler


  def stop(self):
    """
    Stop the scheduler
    """
    if self.scheduler is None:
      msg = "No scheduler found"
      raise AgentRunnerException(msg)
    self.scheduler.stop()
