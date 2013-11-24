#!/usr/bin/env python2
import unittest

from mock import Mock, patch, mock_open
from clu.common.config import classloader


class ClassLoaderTestCase(unittest.TestCase):
  def test_load_class_witouht_module(self):
    """
    Test that a classname without a module raiase an exception
    """
    with self.assertRaisesRegexp(classloader.ClassLoaderException, "No module name found"):
      classloader.load('int')
  
  def test_load_class_empty_modulename(self):
    """
    Test that an empty classname raise an exception
    """
    with self.assertRaisesRegexp(classloader.ClassLoaderException, "No module name found"):
      classloader.load('.clu')
  
  def test_load_class_empty_classname(self):
    """
    Test that an empty classname raise an exception
    """
    with self.assertRaisesRegexp(classloader.ClassLoaderException, "No class name found"):
      classloader.load('clu.')

  def test_load_class(self):
    """
    Test loading a class
    """
    clazz = classloader.load('clu.common.base.Configurable')
    
    from clu.common.base import Configurable
    self.assertTrue(clazz == Configurable)
  
  def test_init_none(self):
    """
    Test init with params None
    """
    with self.assertRaises(classloader.ClassLoaderException): 
      classloader.init(None, None)
  
  def test_init_wrongs_params(self):
    """
    Test init with wrongs params
    """
    clazz = classloader.load('clu.common.base.Configurable')
    with self.assertRaisesRegexp(classloader.ClassLoaderException, "__init__()"):
      instance = classloader.init(clazz, { "onfig" : {"one":1}} )
  
  def test_init(self):
    """
    Test init with params
    """
    clazz = classloader.load('clu.common.base.Configurable')
    instance = classloader.init(clazz, { "config" : {"one":1}} )
    self.assertFalse(instance.config is None)
    self.assertTrue(instance.config.one == 1)


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(ClassLoaderTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
