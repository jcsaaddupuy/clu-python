from clu.probes.mpdprobestatus import MpdProbeStatus
import logging
import time
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

from clu.common.config.agentconfigurator import AgentConfigurator, AgentConfiguratorException
from clu.common.runner.agentrunner import AgentRunner



def main():
  configurator= AgentConfigurator({"folder":"/home/jc", "filename":"clu.conf"})

  configurator.loadfile()
  configurator.loadclasses()
  configurator.initalize_all()

  runners = []
  try:
    for agent in configurator.agents:
      runner = AgentRunner(agent)
      runners.append(runner.start())
    # keep the main thread alive
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt, ex:
    LOGGER.warning("ctrl-C catched, shuting down all threads")
    for runner in runners:
      runner.stop()
      runner.join()
  LOGGER.info("Exiting... bye!")


if __name__=="__main__":
  main()
