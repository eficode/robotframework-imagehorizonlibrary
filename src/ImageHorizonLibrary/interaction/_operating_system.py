# -*- coding: utf-8 -*-
import shlex
import subprocess

from ..errors import OSException


class _OperatingSystem(object):

    def launch_application(self, app, alias=None):
        '''Launches an application.

        Executes the string argument ``app`` as a separate process with
        Python's
        ``[https://docs.python.org/2/library/subprocess.html|subprocess]``
        module. It should therefore be the exact command you would use to
        launch the application from command line.

        On Windows, if you are using relative or absolute paths in ``app``,
        enclose the command with double quotes:

        | Launch Application | "C:\\my folder\\myprogram.exe" | # Needs quotes       |
        | Launch Application | myprogram.exe                  | # No need for quotes |

        Returns automatically generated alias which can be used with `Terminate
        Application`.

        Automatically generated alias can be overridden by providing ``alias``
        yourself.
        '''
        if not alias:
            alias = str(len(self.open_applications))
        process = subprocess.Popen(shlex.split(app))
        self.open_applications[alias] = process
        return alias

    def terminate_application(self, alias=None):
        '''Terminates the process launched with `Launch Application` with
        given ``alias``.

        If no ``alias`` is given, terminates the last process that was
        launched.
        '''
        if alias and alias not in self.open_applications:
            raise OSException('Invalid alias "%s".' % alias)
        process = self.open_applications.pop(alias, None)
        if not process:
            try:
                _, process = self.open_applications.popitem()
            except KeyError:
                raise OSException('`Terminate Application` called without '
                                  '`Launch Application` called first.')
        process.terminate()
