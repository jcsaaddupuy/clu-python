from clu.agents.telnet.telnetagent import TelnetRmqAgent

import logging
LOGGER=logging.getLogger(__name__)

class TelnetProbeStatus(TelnetRmqAgent):
  def __init__(self, config={}, telnetconf={}, rmqconf={}):
    TelnetRmqAgent.__init__(self, config, telnetconf, rmqconf)

  def execute(self):
    telnetclient=self.telnetclient.client
    # Wait for telnet events
    LOGGER.info("Waiting for telnet input")
    
    # will block until data is available
    status=telnetclient.read_some()
    
    LOGGER.info("Got telnet input")
    LOGGER.debug("Status : '%s'"%(status))
    self.basic_publish_json(status)
    LOGGER.info("Published")
