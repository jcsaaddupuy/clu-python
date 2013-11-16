from clu.common.base import CluException

class CluAgentException(CluException):
  pass

class CluAgent(object):
  def run(self):
    raise CluAgentException("Not implemented")

from clu.common.base import Configurable
class ConfigurableCluAgent(Configurable):
  def run(self):
    raise CluAgentException("Not implemented")
