# -*- coding: utf-8 -*-
from os import getcwd, listdir
from os.path import abspath, dirname, isdir, join as path_join
from shutil import rmtree
from sys import exc_info
from tempfile import mkdtemp
from unittest import TestCase

from mock import patch, MagicMock
from robot.libraries.BuiltIn import BuiltIn

CURDIR = abspath(dirname(__file__))


class TestScreenshot(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.patcher = patch.dict('sys.modules', {'pyautogui': self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        self.mock.reset_mock()
        self.patcher.stop()

    def _take_screenshot_many_times(self, expected_filename):
        folder = path_join(CURDIR, 'reference_folder')
        self.lib.set_screenshot_folder(folder)
        for i in range(1, 15):
            self.lib.take_a_screenshot()
            self.mock.screenshot.assert_called_once_with(
                path_join(folder, expected_filename % i))
            self.mock.reset_mock()

    def test_take_a_screenshot(self):
        self._take_screenshot_many_times('ImageHorizon-screenshot-%d.png')

    def test_take_a_screenshot_inside_robot(self):
        with patch.object(BuiltIn, 'get_variable_value',
                          return_value='Suite Name'):
            self._take_screenshot_many_times('SuiteName-screenshot-%d.png')

    def test_take_a_screenshot_with_invalid_folder(self):
        from ImageHorizonLibrary import ScreenshotFolderException

        for index, invalid_folder in enumerate((None, 0, False), 1):
            self.lib.screenshot_folder = invalid_folder
            expected = path_join(getcwd(),
                                 'ImageHorizon-screenshot-%d.png' % index)
            self.lib.take_a_screenshot()
            self.mock.screenshot.assert_called_once_with(expected)
            self.mock.reset_mock()

        for invalid_folder in (123, object()):
            self.lib.screenshot_folder = invalid_folder
            with self.assertRaises(ScreenshotFolderException):
                self.lib.take_a_screenshot()
