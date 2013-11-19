

import test_common_base
import test_clueagent
import test_common_rabbitmq_base
import test_rabbitmqagent

import test_musicplayerdaemon
import test_mpdrmqagent
import test_probe_mpd

import test_xbmc
import test_xbmcagent

import test_telnetclient

def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(test_common_base.suite())
    suite.addTests(test_clueagent.suite())
    suite.addTests(test_common_rabbitmq_base.suite())
    suite.addTests(test_rabbitmqagent.suite())
    suite.addTests(test_mpdrmqagent.suite())
    suite.addTests(test_musicplayerdaemon.suite())
    suite.addTests(test_probe_mpd.suite())
    suite.addTests(test_xbmc.suite())
    suite.addTests(test_xbmcagent.suite())
    suite.addTests(test_telnetclient.suite())
    return suite

if __name__ == '__main__':# pragma: no cover
    unittest.TextTestRunner(verbosity=2).run(suite())
