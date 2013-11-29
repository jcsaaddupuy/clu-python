import logging
LOGGER = logging.getLogger(__name__)

import sys

from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from clu.agents.mpd.mpdclient import MpdClient
import mpd


class MpdRmqException(Exception):
  pass
  
class MpdRmqAgent(RabbitMqAgent):
  def __init__(self, config={}, mpdconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self, config, rmqconf)
    self.mpdclient = MpdClient(mpdconf)
    
    
  def before_execute(self):
    LOGGER.debug("before_execute")
    self.mpdclient.connect()
    RabbitMqAgent.before_execute(self)
  
  def after_execute(self):
    LOGGER.debug("after_execute")
    RabbitMqAgent.after_execute(self)

  def ensure_after_execute(self):
    LOGGER.debug("ensure_after_execute")
    try:
      RabbitMqAgent.ensure_after_execute(self)
    except Exception, ex:
      LOGGER.error("Error on error calling parent ensure_after_execute")
      raise MpdRmqException, MpdRmqException(ex), sys.exc_info()[2] # keep stacktrace
    finally:
      try:
        self.mpdclient.disconnect()
      except Exception, ex2:
        LOGGER.error("Error on error calling disconnect")
        raise MpdRmqException, MpdRmqException(ex2), sys.exc_info()[2] # keep stacktrace

