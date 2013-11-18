from clu.common.base import CluException

class CluAgentException(CluException):
  pass
class CluAgentNotImplementedException(CluException):
  pass

class CluAgent(object):
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
    raise CluAgentNotImplementedException("Not implemented")
  
  def run(self):
    # If before_execute fails, raise the exception
    try:
      self.before_execute()
    except Exception, e:
      raise e
    # if execute() or after_execute() raise an exception,try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(), raise the first exception seen
    ex=None
    try:
      self.execute()
      self.after_execute()
    except Exception, exceptionExecute:
      ex = exceptionExecute
    finally:
      try:
        self.ensure_after_execute()
      except Exception, exceptionAfterExecute:
        if ex is None:
          #ensure the first exception is always raised
          ex = exceptionAfterExecute
      if ex is not None:
        raise ex

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
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
    raise CluAgentNotImplementedException("Not implemented")

  def run(self):
    # If before_execute fails, raise the exception
    try:
      self.before_execute()
    except Exception, e:
      raise e
    # if execute() or after_execute() raise an exception,try to call  ensure_after_execute().
    # if an exception is raised by ensure_after_execute(), raise the first exception seen
    ex=None
    try:
      self.execute()
      self.after_execute()
    except Exception, exceptionExecute:
      ex = exceptionExecute
    finally:
      try:
        self.ensure_after_execute()
      except Exception, exceptionAfterExecute:
        if ex is None:
          #ensure the first exception is always raised
          ex = exceptionAfterExecute
      if ex is not None:
        raise ex