"""Module containing config classes helpers"""
import os
import logging
LOGGER=logging.getLogger(__name__)

import json
from clu.common.base import Configurable
import  importlib

class ConfiguratorException(Exception):
  pass

class Configurator(Configurable):
  def __init__(self,config={}):
    Configurable.__init__(self, config)
    defaults={"filename":None}
    self.__defaults__(defaults)
    self._loadedconfig = None
    self.__clazzs__={}

  def loadfile(self):
    """ Load config file """
    if self.config.filename is None: 
      raise ConfiguratorException("Config file is not defined")
    if not os.path.exists(self.config.filename):
      raise ConfiguratorException("Config file '%s' does not exists"%(self.config.filename))
    LOGGER.info("Loading config file '%s'"%(self.config.filename))
    try:
      f=open(self.config.filename, "r")
      self._loadedconfig = json.load(f)
      f.close()
    except Exception, e:
      raise ConfiguratorException(e)
    
  def loadclasses(self):
    """ Load classes from config """
    if self._loadedconfig is None:
      raise ConfiguratorException("Config not loaded")
    if not self._loadedconfig.has_key("agents"):
      raise ConfiguratorException("Could not find agents in json config")

    for agent in self._loadedconfig["agents"]:
      if not agent.has_key("classname"):
        raise ConfiguratorException("Could not find agent classname json config")
      if not agent.has_key("name"):
        raise ConfiguratorException("Could not find agent name in json config")

      try:
        classparts=agent["classname"].split(".")

        agent_classname= classparts[-1]
        agent_module= ".".join(classparts[0:len(classparts)-1])

        LOGGER.info("Loading module '%s'"%(agent_module))
        module=importlib.import_module(agent_module)

        LOGGER.info("Loading class '%s'"%(agent_classname))
        clazz=getattr(module, agent_classname)
        
        if type(clazz) != type:
          raise ConfiguratorException("'%s' is not a type (%s)"%(agent_classname, type(clazz)))

        self.__clazzs__[agent["name"]]=clazz
      except Exception, e:
        raise ConfiguratorException(e)





  def iniitalize(self, name, configurable):
    """ Load configure """
    pass
