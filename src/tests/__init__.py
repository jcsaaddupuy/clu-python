

import test_common_base
import test_configurableagent
import test_clueagent

import test_rabbitmqclient
import test_rabbitmqagent

import test_mpdclient
import test_mpdrmqagent
import test_mpdprobestatus

import test_xbmcclient
import test_xbmcagent

import test_telnetclient
import test_telnetagent

import test_classloader
import test_configurator
import test_agentconfigurator

import test_agentrunner

def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(test_common_base.suite())
    suite.addTests(test_clueagent.suite())
    
    suite.addTests(test_configurableagent.suite())
    
    suite.addTests(test_rabbitmqclient.suite())
    suite.addTests(test_rabbitmqagent.suite())
    
    suite.addTests(test_mpdclient.suite())
    suite.addTests(test_mpdrmqagent.suite())

    suite.addTests(test_mpdprobestatus.suite())

    suite.addTests(test_xbmcclient.suite())
    suite.addTests(test_xbmcagent.suite())
    
    suite.addTests(test_telnetclient.suite())
    suite.addTests(test_telnetagent.suite())
    
    suite.addTests(test_classloader.suite())
    suite.addTests(test_configurator.suite())
    suite.addTests(test_agentconfigurator.suite())
    
    suite.addTests(test_agentrunner.suite())
    return suite

if __name__ == '__main__':# pragma: no cover
    unittest.TextTestRunner(verbosity=2).run(suite())
