#!/usr/bin/env python2
import unittest
from mock import Mock, MagicMock

from clu.common.base import AutoConfigurableException
from clu.agents import CluAgentException
from clu.agents.mpd.mpdclient import MpdClient, MpdClientException
from mpd import ConnectionError, CommandError, MPDError

class MpdAgentTestCase(unittest.TestCase):

  def test_mpdclient_init_empty_params(self):
    mpdclient = MpdClient()
    self.assertTrue(mpdclient.config.host == "localhost")
    self.assertTrue(mpdclient.config.port == 6600)
    self.assertTrue(mpdclient.config.password is None)

  def test_mpdclient_init_with_mpd_conf(self):
    mpdconf={"host":"host","port":6601}
    mpdclient = MpdClient(mpdconf)

    self.assertTrue(mpdclient.config.host == "host")
    self.assertTrue(mpdclient.config.password is None)
    self.assertTrue(mpdclient.config.port == 6601)

    self.assertTrue(mpdclient.client is not None)

  def test_mpdclient_connect_no_password(self):
    mpdconf={"host":"host","port":6600}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    # Call
    mpdclient.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])

  def test_mpdclient_connect_password(self):
    mpdconf={"host":"host","port":6600, "password":"password"}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    # Call
    mpdclient.connect()
    # Test
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])

  def test_mpdclient_connect_bad_host_raises_mpdclientexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    #Mock the connect method
    connect=Mock(side_effect=ConnectionError())
    mpdmock.connect=connect

    # Call
    with self.assertRaises(MpdClientException):
      mpdclient.connect()


  def test_mpdclient_disconnect_mpdexception_raises_mpdclientexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    #Mock the connect method
    disconnect=Mock(side_effect=MPDError())
    mpdmock.disconnect=disconnect

    # Call
    with self.assertRaises(MpdClientException):
      mpdclient.disconnect()


  def test_mpdclient_connect_bad_password_raises_mpdclientexception(self):
    mpdconf={"host":"badhost","port":6600, "password":"bad_pass"}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    #Mock the password method
    password=Mock(side_effect=CommandError())
    mpdmock.password=password

    # Call
    with self.assertRaises(MpdClientException):
      mpdclient.connect()

    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])
    mpdmock.password.assert_called_with(mpdconf["password"])

  def test_mpdclient_connectexception_raises_mpdclientexception(self):
    mpdconf={"host":"badhost","port":6600}
    mpdclient = MpdClient(mpdconf)

    #Mock the mpd client
    mpdmock=Mock()
    mpdclient.client=mpdmock
    #Mock the connect method and reaise MPDError
    connect=Mock(side_effect=MPDError())
    mpdmock.connect=connect
    # Call
    with self.assertRaises(MpdClientException):
      mpdclient.connect()

    # Methods call assertions
    mpdmock.connect.assert_called_with(mpdconf["host"], mpdconf["port"])


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(MpdAgentTestCase))
  return suite


if __name__ == '__main__': # pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
