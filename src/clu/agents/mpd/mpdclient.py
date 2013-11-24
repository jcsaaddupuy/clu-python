""" Module containing MPD client """
from clu.common.base import Configurable
from clu.agents import CluAgentException

import mpd

import logging
LOGGER = logging.getLogger(__name__)

class MpdClientException(CluAgentException):
  """ Exception raised by MPDClient """
  pass

class MpdClient(Configurable):
  """
  MPD client handler
  """
  def __init__(self, config={}):
    Configurable.__init__(self, config)
    defaults = {
        "host":"localhost",
        "port":6600,
        "password":None
        }
    self.__defaults__(defaults)

    self.client = mpd.MPDClient()

  def connect(self):
    """Connection method """
    LOGGER.debug("Connect")
    try:
      self.client.connect(self.config.host, self.config.port)
      if self.config.password is not None:
        LOGGER.debug("Authentication")
        self.client.password(self.config.password)
    except mpd.ConnectionError, connex:
      LOGGER.exception(connex)
      raise MpdClientException("Connection error on connect", connex)
    except mpd.CommandError, authex:
      LOGGER.exception(authex)
      raise MpdClientException("Authentcation error on connect", authex)
    except mpd.MPDError, unknownex:
      LOGGER.exception(unknownex)
      raise MpdClientException("Unknown MPD error on connect", unknownex)

  def disconnect(self):
    """
    Disconnection method
    """
    LOGGER.debug("MpdClient disconnect")
    try:
      self.client.disconnect()
    except mpd.MPDError, mpdexcept:
      LOGGER.exception(mpdexcept)
      raise MpdClientException("MPD Error on disconnect", mpdexcept)
