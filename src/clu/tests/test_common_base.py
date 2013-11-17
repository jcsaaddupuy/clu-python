#!/usr/bin/env python2
import unittest

from clu.common.base import AutoConfigurable, AutoConfigurableException
from clu.common.base import Configurable


class AutoConfigurableTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = AutoConfigurable()
  
  def test_init_one_kwargs_param(self):
    co = AutoConfigurable(one=1)
    self.assertTrue(co.one == 1)

  def test_init_multiple_kwargs_param(self):
    co = AutoConfigurable(one=1, two=2)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)

  def test_init_one_nodict_args_param(self):
    with self.assertRaises(AutoConfigurableException):
      co = AutoConfigurable('randomstuff')
  
  def test_init_multiples_nodict_args_param(self):
    with self.assertRaises(AutoConfigurableException):
      co = AutoConfigurable('randomstuff', 4,5)
  
  def test_init_one_dict_args_param(self):
    co = AutoConfigurable({'one' : 1})
    self.assertTrue(co.one == 1)

  def test_init_multiple_dict_param(self):
    co = AutoConfigurable({'one':1, 'two':2})
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)


  def test_init_one_nested_kwargs_param(self):
    co = AutoConfigurable({'one':{'two':2}})
    self.assertTrue(co.one.two == 2)

  def test_init_multiples_nested_kwargs_param(self):
    co = AutoConfigurable({'one':{'two':2},'four':{'five':{'six':6}}})
    self.assertTrue(co.one.two == 2)
    self.assertTrue(co.four.five.six == 6)

  def test_with_son(self):
    import simplejson as json # pragma: no cover
    dics = '{"one":{"two":2},"four":{"five":{"six":6}}}'
    dic= json.loads(dics) #pragma: no cover
    co = AutoConfigurable(dic)
    self.assertTrue(co.one.two == 2)
    self.assertTrue(co.four.five.six == 6)
  
  def test_inheritance_simple(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
    co = A(config={"one":1, "two":2})
    self.assertTrue(co.config.one == 1)
    self.assertTrue(co.config.two == 2)
  
  def test_inheritance_noneables(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
        self.__defaults__({"two":None,"three":3})
    co = A(config={"one":1})
    self.assertTrue(co.config.one == 1)
    self.assertTrue(co.config.two is None)
    self.assertTrue(co.config.three == 3)
  
  def test_inheritance_needed(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
        self.__neededs__(("two",))
    with self.assertRaises(AutoConfigurableException):
      co = A(config={"one":1})
  
  def test_configurable_param(self):
    co = Configurable(config={'one':1, 'two':2})
    self.assertFalse(co.config is None)
    self.assertTrue(co.config.one == 1)
    self.assertTrue(co.config.two == 2)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(AutoConfigurableTestCase))
  return suite


if __name__ == '__main__':# pragma: no cover
  unittest.TextTestRunner(verbosity=2).run(suite())
