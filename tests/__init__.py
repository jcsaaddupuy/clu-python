

import test_common_base
import test_common_rabbitmq_base
import test_agents_mpd

def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(test_common_base.suite())
    suite.addTests(test_common_rabbitmq_base.suite())
    suite.addTests(test_agents_mpd.suite())
    return suite

if __name__ == '__main__':# pragma: no cover
    unittest.TextTestRunner(verbosity=2).run(suite())
