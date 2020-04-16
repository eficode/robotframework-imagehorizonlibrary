#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from robot import run_cli

run_cli(sys.argv[1:] + [os.path.dirname(__file__)])
