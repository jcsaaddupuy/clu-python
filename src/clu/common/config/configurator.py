"""Module containing config classes helpers"""
import os
import logging
LOGGER=logging.getLogger(__name__)

import json
from clu.common.base import Configurable
import  importlib
import inspect


class ConfiguratorException(Exception):
  pass

class Configurator(Configurable):
  def __init__(self,config={}):
    Configurable.__init__(self, config)
    defaults={"folder" : None, "filename" : None}
    self.__defaults__(defaults)
    self._loadedconfig = None
    self.__clazzs__={}

    self.agents=[]

  def loadfile(self):
    """ Load config file """
    if self.config.folder is None: 
      raise ConfiguratorException("Config folder is not defined")
    if self.config.filename is None: 
      raise ConfiguratorException("Config file is not defined")
    if not os.path.exists(self.config.filename):
      raise ConfiguratorException("Config file '%s' does not exists"%(self.config.filename))
    LOGGER.info("Loading config file '%s'"%(self.config.filename))
    try:
      fullfilenane = os.path.join(self.config.folder, self.config.filename)
      f=open(self.config.filename, "r")
      self._loadedconfig = json.load(f)
      f.close()
    except Exception, e:
      raise ConfiguratorException(e)
