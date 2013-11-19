import unittest
from mock import Mock, MagicMock
from clu.agents.mpd.mpdagent import MpdRmqAgent
from clu.agents.rabbitmq.rabbitmqagent import RabbitMqAgent

from mock import patch
class MpdRmqAgentTestCase(unittest.TestCase):
  def test_mpdrmq_agent_init(self):
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)
    self.assertFalse(agent.mpdagent is None)
    self.assertTrue(agent.mpdagent.config.host == "mpd.lan")
    self.assertFalse(agent.mpdagent.mpd is None)
    
    self.assertFalse(agent.rmqagent is None)
    self.assertTrue(agent.rmqagent.config.host == "rmq.lan")
  
  def test_mpdrmq_agent_run_call_connect(self):
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    mpdmock=Mock()
    agent.mpdagent=mpdmock

    rmqmock=Mock()
    agent.rmqagent=rmqmock
    # Mock the execute method to get rid of Not implemented exceptions
    execute=Mock()
    agent.execute=execute
    agent.run()

    mpdmock.connect.assert_called()
    mpdmock.connect.assert_called()
    rmqmock.disconnect.assert_called()
    rmqmock.disconnect.assert_called()

  @patch.object(RabbitMqAgent, 'before_execute')
  def test_mpdrmq_before_execute(self, mocked):
    """ Test that the call to before_execute call superclass before_execute"""
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    #Setup generic mock for others methos wich are not tested here
    ignoredmocks=Mock()
    agent.mpdagent=ignoredmocks
    agent.rmqagent=ignoredmocks
    

    instance = mocked.return_value 
    agent.before_execute()
    mocked.assert_called_with(agent)

  
  @patch.object(RabbitMqAgent, 'after_execute')
  def test_mpdrmq_after_execute(self, mocked):
    """ Test that the call to after_execute call superclass after_execute"""
    agentconf={}
    mpdconf={"host":"mpd.lan"}
    rmqconf={"host":"rmq.lan"}
    agent=MpdRmqAgent(agentconf, mpdconf, rmqconf)

    #Setup generic mock for others methods wich are not tested here
    ignoredmocks=Mock()
    agent.mpdagent=ignoredmocks
    agent.rmqagent=ignoredmocks
    

    instance = mocked.return_value 
    agent.after_execute()
    mocked.assert_called_with(agent)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdRmqAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
