# ImageHorizonLibrary

This Robot Framework library provides the facilities to automate GUIs based on image recognition similar to Sikuli. This library wraps [pyautogui](https://github.com/asweigart/pyautogui) to achieve this.

## Keyword documentation

[Keyword Documentation](http://eficode.github.io/robotframework-imagehorizonlibrary/doc/ImageHorizonLibrary.html)

## Prerequisites

- [Python 2.7+](http://python.org) (unfortunately not 3.x)
- [pip](https://pypi.python.org/pypi/pip) for easy installation
- [pyautogui](https://github.com/asweigart/pyautogui) and [it's prerequisites](https://pyautogui.readthedocs.org/en/latest/install.html)
- [Robot Framework](http://robotframework.org)

On OS X, Retina display might [double all coordinates](https://github.com/asweigart/pyautogui/issues/33) from what they are suppose to be. Unfortunately you need to work around this problem yourself.

On Ubuntu, you need to take [special measures](https://pyautogui.readthedocs.org/en/latest/screenshot.html#special-notes-about-ubuntu) to make the screenshot functionality to work correctly. The keyboard functions might not work on Ubuntu when run in VirtualBox on Windows.

### Development

- [mock](http://www.voidspace.org.uk/python/mock/)

## Installation

If you have pip, installation is straightforward

    pip install robotframework-imagehorizonlibrary

This will automatically install dependencies as well as their dependencies.

### OSX

You additionally need to install these for `pyautogui`:

    pip install pyobjc-core pyobjc

For these, you need to install [XCode](https://developer.apple.com/xcode/downloads/)

### Linux

You additionally need to install these for `pyautogui`:

    sudo apt-get install python-dev python-xlib

You might also need, depending on your distribution, to install:

    sudo apt-get install python-tk

If you are using virtualenv, you must install `python-xlib` manually for `pyautogui`.

- [Fetch the source distribution](http://sourceforge.net/projects/python-xlib/files/)
- Install with:
     pip install python-xlib-<latest version>.tar.gz

## Running tests

    python tests/utest/run_tests.py [verbosity=2]

and

    python tests/atest/run_tests.py

