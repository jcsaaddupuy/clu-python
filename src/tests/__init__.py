

import test_common_base
import test_clueagent

import test_rabbitmqclient
import test_rabbitmqagent

import test_mpdclient
import test_mpdrmqagent
import test_mpdprobestatus

import test_xbmcclient
import test_xbmcagent

import test_telnetclient

def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(test_common_base.suite())
    suite.addTests(test_clueagent.suite())
    
    suite.addTests(test_rabbitmqclient.suite())
    suite.addTests(test_rabbitmqagent.suite())
    
    suite.addTests(test_mpdclient.suite())
    suite.addTests(test_mpdrmqagent.suite())

    suite.addTests(test_mpdprobestatus.suite())

    suite.addTests(test_xbmcclient.suite())
    suite.addTests(test_xbmcagent.suite())
    
    suite.addTests(test_telnetclient.suite())
    return suite

if __name__ == '__main__':# pragma: no cover
    unittest.TextTestRunner(verbosity=2).run(suite())
