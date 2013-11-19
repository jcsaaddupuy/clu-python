from clu.agents.mpd.mpdagent import MpdRmqAgent

class MpdProbeStatus(MpdRmqAgent):
  def __init__(self, config={}, mpdconf={}, rmqconf={}):
    MpdRmqAgent.__init__(self, config, mpdconf, rmqconf)

  def execute(self):
    mpdclient=self.mpdclient()
    # Wait for MPD events
    mpdclient.idle()
    status=mpdclient.status()
    self.basic_publish(status)
