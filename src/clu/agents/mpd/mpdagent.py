#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mpdclient import MpdClient
import mpd

import logging
LOGGER=logging.getLogger(__name__)

class MpdRmqException(Exception):
  pass
  
class MpdRmqAgent(RabbitMqAgent):
  def __init__(self, config={}, mpdconf={}, rmqconf={}):
    RabbitMqAgent.__init__(self,config,rmqconf)
    self.mpdclient=MpdClient(mpdconf)
    
    
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
    except Exception, e:
      LOGGER.exception("Error on error calling parent ensure_after_execute", e)
      raise MpdRmqException(e)
    finally:
      try:
        self.mpdclient.disconnect()
      except Exception, e2:
        LOGGER.exception("Error on error calling disconnect", e)
        raise MpdRmqException(e2)

