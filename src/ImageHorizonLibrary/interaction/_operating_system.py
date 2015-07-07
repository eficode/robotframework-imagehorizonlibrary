import subprocess
from platform import platform

PLATFORM = platform()

class OSException(Exception):
    pass

class _OperatingSystem(object):

    def open_application(self, app, *args):
        if PLATFORM.lower().startswith('windows'):
            subprocess.Popen([app]+list(args))
        elif PLATFORM.lower().startswith('darwin'):
            subprocess.Popen(['open', '-a', app, '--args']+list(args))
        #elif PLATFORM.lower().startswith('linux'):
        #    subprocess.Popen([app]+list(args))
        else:
            raise OSException('Unsupported platform.\
                              Supported platforms are:\n\
                              windows, osx') #, linux')
