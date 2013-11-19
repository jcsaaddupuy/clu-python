#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgentException
from clu.agents.mpd.musicplayerdaemon import MusicPlayerDaemon, MusicPlayeraemonEception
from mpd import ConnectionError, CommandError, MPDError

class MpdAgentTestCase(unittest.TestCase):

  def test_mpdagent_init_empty_params(self):
    mpdagent = MusicPlayerDaemon()
    self.assertTrue(mpdagent.config.host == "localhost")
    self.assertTrue(mpdagent.config.port == 6600)
    self.assertTrue(mpdagent.config.password is None)

  def test_mpdagent_init_with_mpd_conf(self):
    mpdconf={"host":"host","port":6601}
    mpdagent = MusicPlayerDaemon(mpdconf)

    self.assertTrue(mpdagent.config.host == "host")
    self.assertTrue(mpdagent.config.password is None)
    self.assertTrue(mpdagent.config.port == 6601)

    self.assertTrue(mpdagent.mpd is not None)

  def test_mpdagent_connect_no_password(self):
    mpdconf={"host":"host","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])

  def test_mpdagent_connect_password(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    # Call
    mpdagent.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])

  def test_mpdagent_connect_bad_host_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method
    connect=Mock(side_effect=ConnectionError())
    mpdmock.connect=connect

    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()


  def test_mpdagent_disconnect_mpdexception_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method
    disconnect=Mock(side_effect=MPDError())
    mpdmock.disconnect=disconnect

    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.disconnect()


  def test_mpdagent_connect_bad_password_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600, "password":"bad_pass"}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the password method
    password=Mock(side_effect=CommandError())
    mpdmock.password=password

    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()

    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])

  def test_mpdagent_connectexception_raises_mpdagentexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdagent = MusicPlayerDaemon(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdagent.mpd=mpdmock
    #Mock the connect method and reaise MPDError
    connect=Mock(side_effect=MPDError())
    mpdmock.connect=connect
    # Call
    with self.assertRaises(MusicPlayeraemonEception):
      mpdagent.connect()

    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
