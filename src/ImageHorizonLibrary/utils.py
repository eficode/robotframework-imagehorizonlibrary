# -*- coding: utf-8 -*-
from platform import platform, architecture


PLATFORM = platform()
ARCHITECTURE = architecture()


def is_windows():
    return PLATFORM.lower().startswith('windows')


def is_mac():
    return PLATFORM.lower().startswith('darwin')


def is_linux():
    return PLATFORM.lower().startswith('linux')


def is_java():
    return PLATFORM.lower().startswith('java')
