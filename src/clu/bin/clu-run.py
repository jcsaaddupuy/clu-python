from clu.probes.mpdprobestatus import MpdProbeStatus
import logging

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

from clu.common.config.configurator import Configurator, ConfiguratorException

configurator= Configurator({"filename":"/home/jc/clu.conf"})

configurator.loadfile()
configurator.loadclasses()
configurator.initalize_all()


#Call
while True:
  configurator.agents[0].run()
