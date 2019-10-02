#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from os.path import abspath, dirname, join as path_join

from robot import run_cli

if __name__ == '__main__':
    curdir = abspath(dirname(__file__))
    sys.path.insert(1, abspath(path_join(curdir, '..', '..', 'src')))
    from ImageHorizonLibrary.utils import *

    if is_windows():
        tag = 'windows'
    elif is_mac():
        tag = 'mac'
    elif is_linux():
        tag = 'linux'

run_cli(sys.argv[1:] + ['--include', tag, '.'])
