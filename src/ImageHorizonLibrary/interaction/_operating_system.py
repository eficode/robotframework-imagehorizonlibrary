import os, subprocess
from platform import platform

PLATFORM = platform()

class OSException(Exception):
    pass

class _OperatingSystem(object):

	def open_application(self, app):
		if PLATFORM.lower().startswith('windows'):
			subprocess.Popen([app])
		elif PLATFORM.lower().startswith('darwin'):
			os.system('open '+app)
		elif PLATFORM.lower().startswith('linux'):
			os.system(app)
		else:
			raise OSException('Unsupported platform.\
							  Supported platforms are:\n\
                              windows, osx, linux')
