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
    try:
      self.execute()
      self.after_execute()
    except Exception, e:
      raise CluAgentException(e)
    finally:
      try:
        self.ensure_after_execute()
      except Exception, e2:
        raise CluAgentException(e2)

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
  def __init__(self, config={}):
    Configurable.__init__(self,config)
    defaults={"name":""}
    self.__defaults__(defaults)
    #create a shortcut
    self.name=self.config.name

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
    try:
      self.execute()
      self.after_execute()
    except Exception, e:
      raise CluAgentException(e)
    finally:
      try:
        self.ensure_after_execute()
      except Exception, e2:
        raise CluAgentException(e2)
