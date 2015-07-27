#!/usr/bin/env python

import sys

from os.path import join as path_join

from robot import run_cli

if __name__ == '__main__':
    sys.path.insert(1, path_join('..', '..', 'src'))
    from ImageHorizonLibrary.utils import *

    if is_windows():
        tag = 'windows'
    elif is_mac():
        tag = 'mac'
    elif is_linux():
        tag = 'linux'

run_cli(sys.argv[1:] + ['--include', tag, '.'])
