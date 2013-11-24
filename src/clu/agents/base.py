""" Module containing bases class for agents """
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
      raise ex
    # if execute() or after_execute() raise an exception,
    # try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(),
    # raise the first exception seen
    try:
      self.execute()
      self.after_execute()
    except Exception, ex:
      raise CluAgentException(ex)
    finally:
      try:
        self.ensure_after_execute()
      except Exception, ex2:
        raise CluAgentException(ex2)

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
  """
  Class representing a CLU agent with configuration
  """
  def __init__(self, config):
    Configurable.__init__(self, config)
    defaults = {"name":""}
    self.__defaults__(defaults)
    #create a shortcut
    self.name = self.config.name

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
      raise ex
    # if execute() or after_execute() raise an exception,
    # try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(),
    # raise the first exception seen
    try:
      self.execute()
      self.after_execute()
    except Exception, ex:
      raise CluAgentException(ex)
    finally:
      try:
        self.ensure_after_execute()
      except Exception, ex2:
        raise CluAgentException(ex2)
