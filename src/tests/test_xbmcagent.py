import unittest
from mock import Mock, MagicMock
from clu.agents.xbmc.xbmcagent import XbmcRmqAgent
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mock import patch
class XbmcRmqAgentTestCase(unittest.TestCase):
  def test_xbmcrmq_agent_init(self):
    agentconf={}
    xbmcconf={"host":"xbmc.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=XbmcRmqAgent(agentconf, xbmcconf, rmqconf)
    self.assertFalse(agent.xbmc is None)
    self.assertTrue(agent.xbmc.config.host == "xbmc.lan")
    
    self.assertFalse(agent.rmq is None)
    self.assertTrue(agent.rmq.config.host == "rmq.lan")
  
  def test_xbmcrmq_agent_xbmcclient(self):
    """ Test that the xbmcclient accessor returns the xbmc.client instance """
    agentconf={}
    xbmcconf={"host":"xbmc.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=XbmcRmqAgent(agentconf, xbmcconf, rmqconf)
    self.assertTrue(agent.xbmc.client == agent.xbmcclient())
    

  @patch.object(RabbitMqAgent, 'before_execute')
  def test_xbmcrmq_before_execute(self, mocked):
    """ Test that the call to before_execute call superclass before_execute"""
    agentconf={}
    xbmcconf={"host":"xbmc.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=XbmcRmqAgent(agentconf, xbmcconf, rmqconf)

    #Setup generic mock for others methos wich are not tested here
    ignoredmocks=Mock()
    agent.xbmc=ignoredmocks
    agent.rmq=ignoredmocks
    

    instance = mocked.return_value 
    agent.before_execute()
    mocked.assert_called_with(agent)

  
  @patch.object(RabbitMqAgent, 'after_execute')
  def test_xbmcrmq_after_execute(self, mocked):
    """ Test that the call to after_execute call superclass after_execute"""
    agentconf={}
    xbmcconf={"host":"xbmc.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=XbmcRmqAgent(agentconf, xbmcconf, rmqconf)

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.xbmc=ignoredmocks
    agent.rmq=ignoredmocks
    

    instance = mocked.return_value 
    agent.after_execute()
    mocked.assert_called_with(agent)
    mocked.assert_called_with(agent)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(XbmcRmqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
