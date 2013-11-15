#!/usr/bin/env python2
import unittest

from clu.common.base import AutoConfigurable, AutoConfigurableException


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

  def test_init_multiple_kwargs_param(self):
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
    import simplejson as json
    dics = '{"one":{"two":2},"four":{"five":{"six":6}}}'
    dic= json.loads(dics)
    co = AutoConfigurable(dic)
    self.assertTrue(co.one.two == 2)
    self.assertTrue(co.four.five.six == 6)
  
  def test_inheritance_simple(self):
    class A(AutoConfigurable):
      def __init__(self, *args, **kwargs):
        AutoConfigurable.__init__(self, *args, **kwargs)
    co = AutoConfigurable(one=1, two=2)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two == 2)
  
  def test_inheritance_noneables(self):
    class A(AutoConfigurable):
      def __init__(self, *args, **kwargs):
        AutoConfigurable.__init__(self, *args, **kwargs)
        self.__nonenables__(("two",))
    co = A(one=1)
    self.assertTrue(co.one == 1)
    self.assertTrue(co.two is None)
  
  def test_inheritance_needed(self):
    class A(AutoConfigurable):
      def __init__(self, *args, **kwargs):
        AutoConfigurable.__init__(self, *args, **kwargs)
        self.__neededattrs__(("two",))
    with self.assertRaises(AutoConfigurableException):
      co = A(one=1)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(AutoConfigurableTestCase))
  return suite


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
