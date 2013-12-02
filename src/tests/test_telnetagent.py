import unittest
from mock import Mock, MagicMock
from clu.agents.telnet.telnetagent import TelnetRmqAgent, TelnetRmqAgenException
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mock import patch
class TelnetRmqAgentTestCase(unittest.TestCase):
  def test_telnetrmq_agent_init(self):
    agentconf={}
    telnetconf={"host":"telnet.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetRmqAgent(agentconf, telnetconf, rmqconf)
    self.assertFalse(agent.telnet is None)
    self.assertTrue(agent.telnet.config.host == "telnet.lan")
    
    self.assertFalse(agent.rmqclient is None)
    self.assertTrue(agent.rmqclient.config.host == "rmq.lan")
  
  def test_telnetrmq_agent_telnetclient(self):
    """ Test that the telnetclient accessor returns the telnet.client instance """
    agentconf={}
    telnetconf={"host":"telnet.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetRmqAgent(agentconf, telnetconf, rmqconf)
    self.assertTrue(agent.telnet.client == agent.telnetclient())
    

  @patch.object(RabbitMqAgent, 'before_execute')
  def test_telnetrmq_before_execute(self, mocked):
    """ Test that the call to before_execute call superclass before_execute"""
    agentconf={}
    telnetconf={"host":"telnet.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetRmqAgent(agentconf, telnetconf, rmqconf)

    #Setup generic mock for others methos wich are not tested here
    ignoredmocks=Mock()
    agent.telnet=ignoredmocks
    agent.rmqclient=ignoredmocks
    

    instance = mocked.return_value 
    agent.before_execute()
    mocked.assert_called_with(agent)

  
  @patch.object(RabbitMqAgent, 'after_execute')
  def test_telnetrmq_after_execute(self, mocked):
    """ Test that the call to after_execute call superclass after_execute"""
    agentconf={}
    telnetconf={"host":"telnet.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetRmqAgent(agentconf, telnetconf, rmqconf)

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.telnet=ignoredmocks
    agent.rmqclient=ignoredmocks
    

    instance = mocked.return_value 
    agent.after_execute()
    mocked.assert_called_with(agent)
    mocked.assert_called_with(agent)
  
  def test_mpdrmq_after_execute_exception(self):
    """ Test that the call to after_execute call superclass after_execute"""
    agentconf={}
    telnetconf={"host":"telnet.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=TelnetRmqAgent(agentconf, telnetconf, rmqconf)

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.telnet=ignoredmocks
    agent.rmqclient=ignoredmocks
    
    agent.telnet.disconnect.side_effect=Exception("In your face")

    with self.assertRaises(TelnetRmqAgenException):
      agent.ensure_after_execute()

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(TelnetRmqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
