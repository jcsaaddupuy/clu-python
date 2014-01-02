#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock
from clu.probes.mpdprobestatus import MpdProbeStatus
import json
from mock import patch

class MpdProbeStatusTestCase(unittest.TestCase):
  def test_mpdprobestatus_statusagent_init(self):
    
    agentconf={"channel":{"exchange":"home.events","type":"fanout"}}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdProbeStatus(agentconf, mpdconf, rmqconf)
    
    self.assertTrue(agent.config is not None)
    self.assertTrue(agent.config.channel.exchange == agentconf["channel"]["exchange"])
    self.assertTrue(agent.config.channel.type == agentconf["channel"]["type"])
    
    self.assertTrue(agent.mpdclient is not None)
    self.assertTrue(agent.mpdclient.config.host == "mpd.lan")
    
    self.assertTrue(agent.rmqclient is not None)
    self.assertTrue(agent.rmqclient.config.host == "rmq.lan")
  
  
  def test_mpdrmq_statusagent_run_readstatus(self):
    agentconf={"channel":{"exchange":"home.events","type":"direct"},"messages":{"routing_key":"home.events.multimedia.music.mpd"}}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdProbeStatus(agentconf, mpdconf, rmqconf)
    
    #Mocks creation
    mockedidle=Mock(return_value=['mixer',])
    mpdstatus={'audio': '44100:24:2',
        'bitrate': '192',
        'consume': '0',
        'elapsed': '168.298',
        'mixrampdb': '0.000000',
        'nextsong': '25',
        'nextsongid': '358',
        'playlist': '411',
        'playlistlength': '60',
        'random': '0',
        'repeat': '0',
        'single': '0',
        'song': '24',
        'songid': '357',
        'state': 'play',
        'time': '168:197',
        'volume': '75'}
    mockedstatus=Mock(return_value=mpdstatus)

    #Mocks binding
    agent.mpdclient.client.idle=mockedidle
    agent.mpdclient.client.status=mockedstatus

    #Setup generic mock for others methos wich are not tested here
    ignoredmocks=Mock()
    agent.mpdclient.connect=ignoredmocks
    agent.mpdclient.disconnect=ignoredmocks
    agent.basic_publish_json = Mock()

    #Call
    agent.run()

    #Tests
    mockedidle.assert_called_once_with()
    mockedstatus.assert_called_with()
    agent.basic_publish_json.assert_called_with(mpdstatus)



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdProbeStatusTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
