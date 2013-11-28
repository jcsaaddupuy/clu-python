"""Module containing config classes helpers"""
import logging
LOGGER = logging.getLogger(__name__)
import sys

import os

import json
from clu.common.base import Configurable


class ConfiguratorException(Exception):
  """
  Exceptions raised by Configurator
  """
  pass


class Configurator(Configurable):
  """
  Class containing config file loading
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults = {"folder" : None, "filename" : None}
    self.__defaults__(defaults)
    self._loadedconfig = None
    self.__clazzs__ = {}

    self.agents = []

  def loadfile(self):
    """ Load config file """
    if self.config.folder is None:
      raise ConfiguratorException("Config folder is not defined")
    if self.config.filename is None:
      raise ConfiguratorException("Config file is not defined")

    fullfilenane = os.path.join(self.config.folder, self.config.filename)
    if not os.path.exists(fullfilenane):
      msg = "Config file '%s' does not exists" % (self.config.filename)
      raise ConfiguratorException(msg)
    LOGGER.info("Loading config file '%s'", self.config.filename)
    try:
      _file = open(fullfilenane, "r")
      self._loadedconfig = json.load(_file)
      _file.close()
    except Exception, ex:
      LOGGER.error("Error disconnecting telnet client")
      raise ConfiguratorException, ConfiguratorException(ex), sys.exc_info()[2] # keep stacktrace
