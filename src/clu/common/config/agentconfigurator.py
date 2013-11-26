"""Module containing config classes helpers"""
import logging
LOGGER = logging.getLogger(__name__)

from clu.common.config.configurator import Configurator
from clu.common.config import classloader

import  importlib


class AgentConfiguratorException(Exception):
  """
  Exceptions raised by AgentConfigurator
  """
  pass

class AgentConfigurator(Configurator):
  """
  Class handling agent configuration
  """
  def __init__(self, config={}):
    Configurator.__init__(self, config)
    defaults = {"filename":"agents.json"}
    self.__defaults__(defaults)
    self.__clazzs__ = {}

    self.agents = []

  def loadclasses(self):
    """ Load classes from config """
    if self._loadedconfig is None:
      raise AgentConfiguratorException("Config not loaded")
    if not self._loadedconfig.has_key("agents"):
      raise AgentConfiguratorException("Could not find agents in json config")

    for agent in self._loadedconfig["agents"]:
      if not agent.has_key("classname"):
        raise AgentConfiguratorException("Could not find agent classname json config")
      if not agent.has_key("name"):
        raise AgentConfiguratorException("Could not find agent name in json config")

      try:
        classname = agent["classname"]
        clazz = classloader.load(classname)
        
        self.__clazzs__[agent["name"]] = clazz
      except Exception, ex:
        raise AgentConfiguratorException(ex)


  def initalize_all(self):
    """ Load configure """
    agents_conf = {}
    if self._loadedconfig.has_key("configs"):
      agents_conf = self._loadedconfig["configs"]
    else:
      LOGGER.debug("No config at all. All Agent will have efault values.")

    for agent_name in self.__clazzs__:
      LOGGER.debug("Initializing '%s'", agent_name)
      conf = {}
      if agents_conf.has_key(agent_name):
        conf = agents_conf[agent_name]
        LOGGER.debug("Found conf for agent '%s'", agent_name)
      else:
        LOGGER.debug("No conf found for agent '%s'", agent_name)
      # Here is the magic : get the Class instance
      clazz = self.__clazzs__[agent_name]
      instance = classloader.init(clazz, conf)
      # We have our instance.
      self.agents.append(instance)
      LOGGER.info("'%s' is fully loaded", agent_name)
