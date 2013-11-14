#!/usr/env/bin python2

class ConfigurableException(Exception):
  pass

class Configurable(object):
  def __init__(self, *args, **kwargs):
    '''If using *args, first argument must be a dictionnary'''
    if len(args) > 1:
      raise ConfigurableException("Only one argument in **args and must be a dict")
    if len(args)> 0 and not type(args[0]) == dict:
      raise ConfigurableException(args)
      raise ConfigurableException("**args must be a dict " + type(args))

    if len(args)>0 :
      for k in args[0]:
        val = args[0][k]
        if type(val)==dict:
          self.__dict__[k]=Configurable(val)
        else:
          self.__dict__[k]=val

    else:
      for k in kwargs:
        val = kwargs[k]
        if type(val)==dict:
          self.__dict__[k]=Configurable(val)
        else:
          self.__dict__[k]=val

