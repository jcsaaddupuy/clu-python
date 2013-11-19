#!/usr/bin/env python2
from clu.common.base import Configurable
from clu.agents import CluAgentException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from xbmcjson import XBMC


class XbmcException(CluAgentException):
  pass

class Xbmc(Configurable):
  """
  XBMC client handler
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults={"host":"localhost", "port":8080, "user":"xbmc", "password":"xbmc"}
    self.__defaults__(defaults)
    self.client=XBMC(self.get_json_rpc(self.config.host), self.config.user, self.config.password)

  def get_json_rpc(self, host):
    jsonrpc="jsonrpc"
    if not host.endswith("/"):
      jsonrpc="/"+jsonrpc
    return host+jsonrpc
