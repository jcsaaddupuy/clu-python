""" Module containing bases class for agents """
import logging
LOGGER = logging.getLogger(__name__)
import sys

from clu.common.base import CluException


class CluAgentException(CluException):
  """Exceptions raised by CluAgent """
  pass
class CluAgentNotImplementedException(CluException):
  """Exceptions raised by CluAgent """
  pass

class CluAgent(object):
  """
  Class representing a CLU agent
  """
  def before_execute(self):
    """
    Executed before the method execute.
    If this method fails, execute won't be called.
    """
    pass
  def after_execute(self):
    """
    Executed after the method execute
    """
    pass

  def ensure_after_execute(self):
    """
    Executed after the method execute even if exceptions occurs
    """
    pass

  def execute(self):
    """ Method executing any processing """
    raise CluAgentNotImplementedException("Not implemented")

  def run(self):
    """ This method call before_execute, run, after_execute, ensure_after_execute"""
    # If before_execute fails, raise the exception
    try:
      self.before_execute()
    except Exception, ex:
      raise CluAgentException, CluAgentException(ex), sys.exc_info()[2] # keep stacktrace
    # if execute() or after_execute() raise an exception,
    # try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(),
    # raise the first exception seen
    try:
      self.execute()
      self.after_execute()
    except Exception, ex:
      raise CluAgentException, CluAgentException(ex), sys.exc_info()[2] # keep stacktrace
    finally:
      try:
        self.ensure_after_execute()
      except Exception, ex2:
        raise CluAgentException, CluAgentException(ex2), sys.exc_info()[2] # keep stacktrace

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
  """
  Class representing a CLU agent with configuration
  """
  def __init__(self, config):
    Configurable.__init__(self, config)
    defaults = {"name":"", "id":None, "scheduling":None}
    self.__defaults__(defaults)
    #create a shortcut
    self.name = self.config.name
    self.id = self.config.id

  def before_execute(self):
    """Executed before the method execute. If this method fails, execute won't be called."""
    pass
  def after_execute(self):
    """Executed after the method execute"""
    pass
  def ensure_after_execute(self):
    """Executed after the method execute even if exceptions occurs"""
    pass
  def execute(self):
    """ Method executing any processing """
    raise CluAgentNotImplementedException("Not implemented (%s)"%(self.__class__))

  def run(self):
    """ This method call before_execute, run, after_execute, ensure_after_execute"""
    # If before_execute fails, raise the exception
    try:
      self.before_execute()
    except Exception, ex:
      LOGGER.error(ex)
      try:
        self.ensure_after_execute()
      except Exception, ex2:
        LOGGER.exception(ex2)
        raise CluAgentException, CluAgentException(ex2), sys.exc_info()[2] # keep stacktrace
      raise CluAgentException, CluAgentException(ex), sys.exc_info()[2] # keep stacktrace
    # if execute() or after_execute() raise an exception,
    # try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(),
    # raise the first exception seen
    try:
      self.execute()
      self.after_execute()
    except Exception, ex:
      LOGGER.error(ex)
      raise CluAgentException, CluAgentException(ex), sys.exc_info()[2] # keep stacktrace
    finally:
      try:
        self.ensure_after_execute()
      except Exception, ex2:
        LOGGER.error(ex2)
        raise CluAgentException, CluAgentException(ex2), sys.exc_info()[2] # keep stacktrace
