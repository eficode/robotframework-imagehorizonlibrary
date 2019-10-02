#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from os.path import abspath, dirname, join as path_join
from unittest import TestLoader, TextTestRunner

directory = dirname(__file__)
path = path_join(abspath(path_join(directory, '..', '..', 'src')))
sys.path.insert(1, path)

try:
    import mock
except ImportError:
    raise ImportError('Please install mock')

if len(sys.argv) > 1 and 'verbosity=' in sys.argv[1]:
    verbosity = int(sys.argv[1].split('=')[1])
else:
    verbosity = 1

sys.exit(not TextTestRunner(verbosity=verbosity).run(TestLoader().discover(directory)).wasSuccessful())
