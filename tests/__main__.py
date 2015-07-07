import sys
from os.path import abspath, dirname, join as path_join


path = abspath(path_join(dirname(__file__), '..', 'src'))
sys.path.insert(1, path)

from ImageHorizonLibrary import utils

# Import correct tests depending on platform
if utils.is_windows():
	from windows.tests import main as test_main
elif utils.is_mac():
    from mac.tests import main as test_main
elif utils.is_linux():
    from linux.tests import main as test_main

test_main()
