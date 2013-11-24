"""Module containing ClassLoader utils"""
import  importlib

import logging
LOGGER = logging.getLogger(__name__)


class ClassLoaderException(Exception):
  """
  Exceptions raise by ClassLoader
  """
  pass

def load(classname):
  """
  Load a class from it full qualified name
  :param classname: The full qualified classname for the class to load
  :return: The class object
  """
  try:
    classparts = classname.split(".")
    agent_classname = classparts[-1]
    agent_module = ".".join(classparts[0:len(classparts)-1])

    if agent_module == "":
      raise ClassLoaderException("No module name found")
    if agent_classname == "":
      raise ClassLoaderException("No class name found")

    LOGGER.info("Loading module '%s'", agent_module)
    module = importlib.import_module(agent_module)

    LOGGER.info("Loading class '%s'", agent_classname)
    clazz = getattr(module, agent_classname)

    if type(clazz) != type:
      raise ClassLoaderException("%s is not a type" % (clazz))


    return clazz
  except Exception, excep:
    raise ClassLoaderException(excep)

def init(clazz, params):
  """
  Initialize an instance of the given class with the given parameters
  :param clazz: The class we want to instanciate
  :param param: Dictionary containing parameters
                which will be passed to the constructor
  :return: An instance of clazz
  """
  try:
    return clazz(**params)
  except Exception, excep:
    raise ClassLoaderException(excep)
