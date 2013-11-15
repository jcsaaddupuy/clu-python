#!/usr/bin/env python2
import unittest

from clu.common.base import Configurable, ConfigurableException


class ConfigurableTestCase(unittest.TestCase):

  def test_init_empty_params(self):
    confgigurable = Configurable()
  
  def test_init_one_kwargs_param(self):
    co = Configurable(one=1)
    self.assertTrue(co.one == 1)

  def test_init_multiple_kwargs_param(self):
    co = Configurable(one=1, two=2)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)

  def test_init_one_nodict_args_param(self):
    with self.assertRaises(ConfigurableException):
      co = Configurable('randomstuff')
  
  def test_init_multiples_nodict_args_param(self):
    with self.assertRaises(ConfigurableException):
      co = Configurable('randomstuff', 4,5)
  
  def test_init_one_dict_args_param(self):
    co = Configurable({'one' : 1})
    self.assertTrue(co.one == 1)

  def test_init_multiple_kwargs_param(self):
    co = Configurable({'one':1, 'two':2})
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)


  def test_init_one_nested_kwargs_param(self):
    co = Configurable({'one':{'two':2}})
    self.assertTrue(co.one.two == 2)

  def test_init_multiples_nested_kwargs_param(self):
    co = Configurable({'one':{'two':2},'four':{'five':{'six':6}}})
    self.assertTrue(co.one.two == 2)
    self.assertTrue(co.four.five.six == 6)

  def test_with_son(self):
    import simplejson as json
    dics = '{"one":{"two":2},"four":{"five":{"six":6}}}'
    dic= json.loads(dics)
    co = Configurable(dic)
    self.assertTrue(co.one.two == 2)
    self.assertTrue(co.four.five.six == 6)
  
  def test_inheritance_simple(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
    co = Configurable(one=1, two=2)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)
  
  def test_inheritance_noneables(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
        self.__nonenables__(("two",))
    co = A(one=1)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two is None)
  
  def test_inheritance_needed(self):
    class A(Configurable):
      def __init__(self, *args, **kwargs):
        Configurable.__init__(self, *args, **kwargs)
        self.__neededattrs__(("two",))
    with self.assertRaises(ConfigurableException):
      co = A(one=1)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(ConfigurableTestCase))
  return suite


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
