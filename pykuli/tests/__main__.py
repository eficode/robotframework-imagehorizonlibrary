import sys
from platform import platform, architecture

PLATFORM = platform()
ARCHITECTURE = architecture()

# Import correct tests depending on platform
if PLATFORM.lower().startswith('windows'):
	from pykuli.tests.windows.tests import main as test_main

test_main()

