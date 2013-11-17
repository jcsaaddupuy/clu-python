#!/usr/env/bin python2

class AutoConfigurableException(Exception):
  pass

class AutoConfigurable(object):
  ''' Ths classs allow to valorize attributes with any given parameters'''

  def __init__(self, *args, **kwargs):
    '''If using *args, first argument must be a dictionnary'''
    if len(args) > 1:
      raise AutoConfigurableException("Only one argument in *args and must be a dict")
    if len(args)> 0 and not type(args[0]) == dict:
      raise AutoConfigurableException("**args must be a dict ")

    myattr={}
    if len(args)>0 :
      myattr=args[0]
    else:
      myattr=kwargs

    for k in myattr:
      val = myattr[k]
      if type(val)==dict:
        self.__dict__[k]=AutoConfigurable(val)
      else:
        self.__dict__[k]=val


class Configurable(object):
  def __init__(self, config={}):
    self.config=AutoConfigurable(config)
  
  def __neededs__(self, needed=()):
    for k in needed:
      if not self.config.__dict__.has_key(k):
        raise AutoConfigurableException("missing %s"%(k))

  def __defaults__(self, defaults={}):
    for k in defaults:
      if not self.config.__dict__.has_key(k):
        val=defaults[k]
        if type(val)==dict:
          self.config.__dict__[k]=AutoConfigurable(val)
        else:
          self.config.__dict__[k]=val

