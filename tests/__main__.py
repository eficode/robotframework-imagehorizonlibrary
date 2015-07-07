import sys

from os.path import abspath, dirname, join as path_join
from platform import platform, architecture

path = abspath(path_join(dirname(__file__), '..', 'src'))
sys.path.insert(1, path)


PLATFORM = platform()
ARCHITECTURE = architecture()

# Import correct tests depending on platform
if PLATFORM.lower().startswith('windows'):
	from windows.tests import main as test_main
elif PLATFORM.lower().startswith('darwin'):
    from mac.tests import main as test_main
elif PLATFORM.lower().startswith('linux'):
    from linux.tests import main as test_main
    
test_main()
