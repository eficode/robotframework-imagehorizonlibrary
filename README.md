# ImageHorizonLibrary

This Robot Framework library provides the facilities to automate GUIs based on image recognition similar to Sikuli. This library wraps [pyautogui](https://github.com/asweigart/pyautogui) to achieve this.

## Prerequisites

- [Python 2.7+](http://python.org) (unfortunately not 3.x)
- [pip](https://pypi.python.org/pypi/pip) for easy installation
- [pyautogui](https://github.com/asweigart/pyautogui) and it's prerequisites
- [Robot Framework](http://robotframework.org)

### Development

- [mock](http://www.voidspace.org.uk/python/mock/)

## Installation

If you have pip, installation is straightforward

    pip install pyautogui robotframework robotframework-imagehorizonlibrary

### OSX

Install [XCode](https://developer.apple.com/xcode/downloads/)

    pip install pyobjc-core pyobjc

### Linux

    sudo apt-get install python-dev python-xlib

## Running tests

    python tests/utest/run_tests.py [verbosity=2]

and

    python tests/atest/run_tests.py

