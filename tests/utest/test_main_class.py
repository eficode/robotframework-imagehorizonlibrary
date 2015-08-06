# -*- coding: utf-8 -*-
import os
import shlex

from os.path import abspath, dirname, join as path_join
from subprocess import PIPE, Popen
from unittest import SkipTest, TestCase
from warnings import warn

from mock import MagicMock, patch


SRCDIR = path_join(abspath(dirname(__file__)), '..', '..', 'src')

class TestMainClass(TestCase):
    def setUp(self):
        self.pyautogui_mock = MagicMock()
        self.Tk_mock = MagicMock()
        self.clipboard_mock = MagicMock()
        self.clipboard_mock.clipboard_get.return_value = 'copied text'
        self.Tk_mock.Tk.return_value = self.clipboard_mock
        self.patcher = patch.dict('sys.modules',
                                  {'pyautogui' : self.pyautogui_mock,
                                   'Tkinter' : self.Tk_mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        for mock in (self.Tk_mock, self.clipboard_mock, self.pyautogui_mock):
            mock.reset_mock()
        self.patcher.stop()

    def test_copy(self):
        from ImageHorizonLibrary import ImageHorizonLibrary

        with patch.object(ImageHorizonLibrary, '_press') as press_mock:
            retval = self.lib.copy()
            self.assertEquals(retval, 'copied text')
            self.clipboard_mock.clipboard_get.assert_called_once_with()
            if self.lib.is_mac:
                press_mock.assert_called_once_with('Key.command', 'c')
            else:
                press_mock.assert_called_once_with('Key.ctrl', 'c')

    def test_alert(self):
        self.lib.pause()
        self.pyautogui_mock.alert.assert_called_once_with(
            button='Continue', text='Test execution paused.', title='Pause')

    def _get_cmd(self, jython, path):
        cmd = ('JYTHONPATH={path} {jython} -c '
               '"from ImageHorizonLibrary import ImageHorizonLibrary"')
        return cmd.format(jython=jython, path=path)

    def test_importing_fails_on_java(self):
        # This test checks that importing fails when any of the dependencies
        # are not installed or, at least, importing Tkinter fails because
        # it's not supported on Jython.
        if not 'JYTHON_HOME' in os.environ:
            self.skipTest('%s() was not run because JYTHON_HOME was not set.' % self._testMethodName)
        jython_cmd = path_join(os.environ['JYTHON_HOME'], 'bin', 'jython')
        cmd = self._get_cmd(jython_cmd, SRCDIR)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        _, stderr = p.communicate()
        self.assertNotEqual(stderr, '')

