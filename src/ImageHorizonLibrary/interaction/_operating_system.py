import shlex
import subprocess

class OSException(Exception):
    pass

class _OperatingSystem(object):

    def launch_application(self, app, alias=None):
        if not alias:
            alias = str(len(self.open_applications))
        process = subprocess.Popen(shlex.split(app))
        self.open_applications[alias] = process
        return alias

    def terminate_application(self, alias=None):
        if not alias:
            alias = str(len(self.open_applications)-1)
        if not alias in self.open_applications:
            raise OSException('Invalid alias "%s".' % alias)
        self.open_applications[alias].terminate()
        self.open_applications.pop(alias)


        