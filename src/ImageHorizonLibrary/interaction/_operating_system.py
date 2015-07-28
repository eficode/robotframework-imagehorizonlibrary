# -*- coding: utf-8 -*-
import shlex
import subprocess

from ..errors import OSException

class _OperatingSystem(object):

    def launch_application(self, app, alias=None):
        '''
        Launches an application.
        Executes the string argument 'app' as a subprocess.
        Returns alias, which is a reference to the subprocess
        and can be passed to terminate application. Alias can be overridden
        by providing argument alias.

        Warning:
        If the app itself launches processes in the background,
        like 'open' in OSX, they cannot be terminated returned with alias.
        '''
        if not alias:
            alias = str(len(self.open_applications))
        process = subprocess.Popen(shlex.split(app))
        self.open_applications[alias] = process
        return alias

    def terminate_application(self, alias=None):
        '''
        Terminates the last app that was launched with launch_application,
        or the app corresponding to alias if alias is given.
        '''
        if alias and not alias in self.open_applications:
            raise OSException('Invalid alias "%s".' % alias)
        process = self.open_applications.pop(alias, None)
        if not process:
            try:
                _, process = self.open_applications.popitem()
            except KeyError:
                raise OSException('`Terminate Application` called without '
                            '`Launch Application` called first.')
        process.terminate()


