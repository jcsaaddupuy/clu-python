from clu.agents.mpd.mpdagent import MpdRmqAgent

import logging
LOGGER=logging.getLogger(__name__)

class MpdProbeStatus(MpdRmqAgent):
  def __init__(self, config={}, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, config, mpdconf, rmqconf)

  def execute(self):
    mpdclient=self.mpdclient.client
    # Wait for MPD events
    LOGGER.info("Waiting for mpd status change")
    mpdclient.idle()
    status=mpdclient.status()
    LOGGER.info("Got MPD status")
    LOGGER.debug("Status : '%s'"%(status))
    self.basic_publish(status)
    LOGGER.info("Published")
