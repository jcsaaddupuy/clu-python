#!/usr/bin/env python                                                                                                                                        
from setuptools import setup, find_packages

setup(name='clu',
    version='0.1',
    description='CLU home automation system',
    author='JC',
    # Package structure
    #
    # find_packages searches through a set of directories 
    # looking for packages
    packages = find_packages('src', exclude = ['ez_setup',
      '*.tests', '*.tests.*', 'tests.*', 'tests']),
    # package_dir directive maps package names to directories.
    # package_name:package_directory
    package_dir = {'': 'src'},
    install_requires = ["python-mpd >= 0.3.0"],


    # Tests
    #
    # Tests must be wrapped in a unittest test suite by either a
    # function, a TestCase class or method, or a module or package
    # containing TestCase classes. If the named suite is a package,
    # any submodules and subpackages are recursively added to the
    # overall test suite.
    test_suite = 'tests.suite',
    tests_require = ['simplejson', 'mock', 'coverage'],

    )
