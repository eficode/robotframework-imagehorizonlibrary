#!/usr/bin/env python
import sys
import unittest
from os.path import abspath, dirname, join as path_join

directory = dirname(__file__)
path = path_join(abspath(path_join(directory, '..', '..', 'src')))
sys.path.insert(1, path)

try:
    import mock
except ImportError:
    raise ImportError('Please install mock')

unittest.TextTestRunner().run(unittest.TestLoader().discover(directory))

