""" Module containing MPD client """
import logging
LOGGER = logging.getLogger(__name__)

import sys
from clu.common.base import Configurable
from clu.agents import CluAgentException

import mpd


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
    LOGGER.info("Connect MPD client")
    try:
      self.client.connect(self.config.host, self.config.port)
      if self.config.password is not None:
        LOGGER.debug("Authentication")
        self.client.password(self.config.password)
    except mpd.ConnectionError, connex:
      LOGGER.error("Connection error on connect")
      raise MpdClientException, MpdClientException(connex), sys.exc_info()[2] # keep stacktrace
    except mpd.CommandError, authex:
      LOGGER.error("Authentcation error on connect")
      raise MpdClientException, MpdClientException(authex), sys.exc_info()[2] # keep stacktrace
    except mpd.MPDError, unknownex:
      LOGGER.error("Unknown MPD error on connect")
      raise MpdClientException, MpdClientException(unknownex), sys.exc_info()[2] # keep stacktrace

  def disconnect(self):
    """
    Disconnection method
    """
    LOGGER.debug("MpdClient disconnect")
    try:
      if self.client is not None:
        LOGGER.info("Disconnecting MPD client")
        self.client.disconnect()
      else:
        LOGGER.debug("MPD client was None, didn't disconnected it.")

    except mpd.ConnectionError, e:
      LOGGER.error("Error on error calling disconnect")
    except mpd.MPDError, mpdexcept:
      LOGGER.error("MPD Error on disconnect")
      raise MpdClientException, MpdClientException(mpdexcept), sys.exc_info()[2] # keep stacktrace
