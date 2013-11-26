""" Module containing agent runner """
import time
import logging
LOGGER = logging.getLogger(__name__)
from clu.common.base import Configurable

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

class LoopScheduler(object):
  """
  Execute an agent inside a loop
  """
  def __init__(self, instance = None, wait = 0.5, max_retry = 3):
    self.wait = wait
    self.instance = instance
    self.is_stopped = False

    self.max_retry = max_retry
    self.tryed = 0

  def start(self):
    """ starts the agent """
    LOGGER.info("Starting LoopScheduler for '%s'", self.instance)

    while not self.is_stopped and not self.max_retry_reached():
      self.tryed += 1
      try:
        self.instance.run()
      except Exception, ex:
        LOGGER.error("Error while running agent (%s/%s). %s", self.tryed, self.max_retry, ex)
      time.sleep(self.wait)

  def stop(self):
    """ Stop the agent """
    self.is_stopped = True

  def max_retry_reached(self):
    return self.tryed >= self.max_retry

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


  def stop(self):
    """
    Stop the scheduler
    """
    if self.scheduler is None:
      msg = "No scheduler found"
      raise AgentRunnerException(msg)
    self.scheduler.stop()
