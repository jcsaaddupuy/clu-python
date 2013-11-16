from clu.common.base import CluException

class CluAgentException(CluException):
  pass
class CluAgentNotImplementedException(CluException):
  pass

class CluAgent(object):
  def before_execute(self):
    pass
  def after_execute(self):
    pass
  def execute(self):
    raise CluAgentNotImplementedException("Not implemented")
  
  def run(self):
    self.before_execute()
    self.execute()
    self.after_execute()

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
  def before_execute(self):
    pass
  def after_execute(self):
    pass
  def execute(self):
    raise CluAgentNotImplementedException("Not implemented")
  def run(self):
    self.before_execute()
    self.execute()
    self.after_execute()
