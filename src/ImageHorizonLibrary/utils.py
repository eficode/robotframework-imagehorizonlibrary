# -*- coding: utf-8 -*-
from platform import platform, architecture
from subprocess import call


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

def has_retina():
    if is_mac():
        # Will return 0 if there is a retina display
        return_code = call("system_profiler SPDisplaysDataType | grep 'Retina'", shell=True)
        return not return_code
    return 0
