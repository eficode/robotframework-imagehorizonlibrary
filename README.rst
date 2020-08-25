===================
ImageHorizonLibrary
===================

This Robot Framework library provides the facilities to automate GUIs based on
image recognition similar to Sikuli. This library wraps pyautogui_ to achieve
this.

For non pixel perfect matches, there is a feature called `confidence level`
that comes with a dependency OpenCV (python package: `opencv-python`).
This functionality is optional - you are not required to
install `opencv-python` package if you do not use confidence level.

Keyword documentation
---------------------

`Keyword Documentation`__

__ http://eficode.github.io/robotframework-imagehorizonlibrary/doc/ImageHorizonLibrary.html

Travis CI
---------

`Travis CI`__

__ https://travis-ci.org/Eficode/robotframework-imagehorizonlibrary/


.. image:: https://travis-ci.org/Eficode/robotframework-imagehorizonlibrary.svg?branch=master
    :target: https://travis-ci.org/Eficode/robotframework-imagehorizonlibrary


Prerequisites
-------------

- `Python 3.x`
- pip_ for easy installation
- pyautogui_ and `it's prerequisites`_
- `Robot Framework`_

On Ubuntu, you need to take `special measures`_ to make the screenshot
functionality to work correctly. The keyboard functions might not work on
Ubuntu when run in VirtualBox on Windows.

Development
'''''''''''

- mock__

__ http://www.voidspace.org.uk/python/mock/

Installation
------------

If you have pip_, installation is straightforward:

::

    $ pip install robotframework-imagehorizonlibrary

This will automatically install dependencies as well as their dependencies.


Windows
'''''''

ImageHorizonLibrary should work on Windows "out-of-the-box". Just run the
commands above to install it.

OSX
'''

*NOTICE*
ImageHorizonLibrary does not currently work with XCode v.8. Please use a previous version.

You additionally need to install these for pyautogui_:

::

    $ pip install pyobjc-core pyobjc


For these, you need to install XCode_

Linux
'''''

You additionally need to install these for pyautogui_:

::

    $ sudo apt-get install python-dev python-xlib


You might also need, depending on your Python distribution, to install:

::

    $ sudo apt-get install python-tk

If you are using virtualenv, you must install python-xlib_ manually to the
virtual environment for pyautogui_:

- `Fetch the source distribution`_
- Install with:

::

    $ pip install python-xlib-<latest version>.tar.gz

Running unit tests
------------------

::

    $ python tests/utest/run_tests.py [verbosity=2]


Running acceptance tests
------------------------

Additionally to unit test dependencies, you also need OpenCV, Eel, scrot and Chrome/Chromium browser.
OpenCV is used because this tests are testing also confidence level.
Browser is used by Eel for cross-platform GUI demo application.
scrot is used for capturing screenshots.

::
    $ pip install opencv-python eel


To run tests, run this command:

::

    $ python tests/atest/run_tests.py


Updating Docs
-------------

To regenerate documentation (`doc/ImageHorizonLibrary.html`), use this command:

::

    $ python -m robot.libdoc -P ./src ImageHorizonLibrary doc/ImageHorizonLibrary.html


.. _Python 3.x: http://python.org
.. _pip: https://pypi.python.org/pypi/pip
.. _pyautogui: https://github.com/asweigart/pyautogui
.. _it's prerequisites: https://pyautogui.readthedocs.org/en/latest/install.html
.. _Robot Framework: http://robotframework.org
.. _double all coordinates: https://github.com/asweigart/pyautogui/issues/33
.. _special measures: https://pyautogui.readthedocs.org/en/latest/screenshot.html#special-notes-about-ubuntu
.. _XCode: https://developer.apple.com/xcode/downloads/
.. _Fetch the source distribution:
.. _python-xlib: http://sourceforge.net/projects/python-xlib/files/

