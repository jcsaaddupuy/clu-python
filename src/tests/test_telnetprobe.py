#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock
from clu.probes.telnetprobe import TelnetProbeStatus
import json
from mock import patch

class TelnetProbeStatusTestCase(unittest.TestCase):
  def test_telnetprobestatus_statusagent_init(self):
    
    agentconf={"channel":{"exchange":"home.events","type":"fanout"}}
    telnetconf={"host":"telnet.lan", "port":20000}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetProbeStatus(agentconf, telnetconf, rmqconf)
    
    self.assertTrue(agent.config is not None)
    self.assertTrue(agent.config.channel.exchange == agentconf["channel"]["exchange"])
    self.assertTrue(agent.config.channel.type == agentconf["channel"]["type"])
    
    self.assertTrue(agent.telnetclient is not None)
    self.assertTrue(agent.telnetclient.config.host == "telnet.lan")
    self.assertTrue(agent.telnetclient.config.port == 20000)
    
    self.assertTrue(agent.rmqclient is not None)
    self.assertTrue(agent.rmqclient.config.host == "rmq.lan")
  
  
  def test_telnetrmq_statusagent_run_readstatus(self):
    agentconf={"channel":{"exchange":"home.events","type":"direct"},"messages":{"routing_key":"home.events.multimedia.music.telnet"}}
    telnetconf={"host":"telnet.lan", "port":20000}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetProbeStatus(agentconf, telnetconf, rmqconf)
    
    #Mocks creation
    telnetstatus="data data"
    mockedreaduntil=Mock(return_value=telnetstatus)

    #Mocks binding
    agent.telnetclient = Mock()
    agent.telnetclient.client.read_some=mockedreaduntil

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.telnetclient.connect=ignoredmocks
    agent.telnetclient.disconnect=ignoredmocks
    agent.basic_publish_json = Mock()

    #Call
    agent.run()

    #Tests
    mockedreaduntil.assert_called_with()
    agent.basic_publish_json.assert_called_with(telnetstatus)



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(TelnetProbeStatusTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
