#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents.mpd.mpdagent import MpdControl, MpdStatus


class MpdAgentsTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = MpdControl()
  
  def test_init_status_full_param(self):
    co = MpdStatus(host="host", port=6600, password="password", rmq_host="rmq_host", rmq_password="rmq_password", rmq_port=4444)
    self.assertTrue(co.host == "host")
    self.assertTrue(co.password == "password")
    self.assertTrue(co.port == 6600)
    
    self.assertFalse(co.mpd is None)
    
    self.assertFalse(co.rabbit is None)
    self.assertTrue(co.rabbit.host == "rmq_host")
    self.assertTrue(co.rabbit.password == "rmq_password")
    self.assertTrue(co.rabbit.port == 4444)

  def test_init_control_full_param(self):
    co = MpdControl(host="host", port=6600, password="password", rmq_host="rmq_host", rmq_password="rmq_password", rmq_port=4444)
    self.assertTrue(co.host == "host")
    self.assertTrue(co.password == "password")
    self.assertTrue(co.port == 6600)
    
    self.assertFalse(co.mpd is None)
    
    self.assertFalse(co.rabbit is None)
    self.assertTrue(co.rabbit.host == "rmq_host")
    self.assertTrue(co.rabbit.password == "rmq_password")
    self.assertTrue(co.rabbit.port == 4444)



def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentsTestCase))
  return suite


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
