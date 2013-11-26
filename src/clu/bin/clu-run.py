from clu.probes.mpdprobestatus import MpdProbeStatus
import logging

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

from clu.common.config.agentconfigurator import AgentConfigurator, AgentConfiguratorException
from clu.common.runner.agentrunner import AgentRunner


configurator= AgentConfigurator({"folder":"/home/jc", "filename":"clu.conf"})

configurator.loadfile()
configurator.loadclasses()
configurator.initalize_all()

runners = []

for agent in configurator.agents:
  print agent
  runner = AgentRunner(agent)
  runners.append(runner)
  runner.start()
