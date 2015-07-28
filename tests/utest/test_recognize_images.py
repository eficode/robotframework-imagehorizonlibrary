# -*- coding: utf-8 -*-
import time

from unittest import TestCase
from os.path import abspath, dirname, join as path_join
from mock import call, MagicMock, patch

CURDIR = abspath(dirname(__file__))
TESTIMG_DIR = path_join(CURDIR, 'reference_images')

class TestRecognizeImages(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.patcher = patch.dict('sys.modules', {'pyautogui' : self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary(reference_folder=TESTIMG_DIR)
        self.locate = 'ImageHorizonLibrary.ImageHorizonLibrary.locate'
        self._locate = 'ImageHorizonLibrary.ImageHorizonLibrary._locate'

    def tearDown(self):
        self.mock.reset_mock()
        self.patcher.stop()

    def test_click_image(self):
        with patch(self.locate, return_value=(0,0)):
            self.lib.click_image('doesentmatter')
            self.mock.click.assert_called_once_with((0,0))

    def _call_all_directional_functions(self, fn_name):
        from ImageHorizonLibrary import ImageHorizonLibrary
        retvals = []
        for direction in ['above', 'below', 'left', 'right']:
            fn = getattr(self.lib, fn_name % direction)
            with patch(self.locate, return_value=(0,0)):
                retvals.append(fn('doesentmatter', 10))
        return retvals

    def _verify_calls_to_pyautogui(self, mock_calls, clicks=1):
        self.assertEquals(
            mock_calls,
            [call(0, -10, button='left', interval=0.0, clicks=clicks),
             call(0, 10, button='left', interval=0.0, clicks=clicks),
             call(-10, 0, button='left', interval=0.0, clicks=clicks),
             call(10, 0, button='left', interval=0.0, clicks=clicks)])

    def test_directional_clicks(self):
        self._call_all_directional_functions('click_to_the_%s_of_image')
        self._verify_calls_to_pyautogui(self.mock.click.mock_calls)

    def test_directional_copies(self):
        copy = 'ImageHorizonLibrary.ImageHorizonLibrary.copy'
        with patch(copy, return_value='Some Text'):
            ret = self._call_all_directional_functions('copy_from_the_%s_of')
        self._verify_calls_to_pyautogui(self.mock.click.mock_calls, clicks=3)
        for retval in ret:
            self.assertEquals(retval, 'Some Text')

    def test_does_exist(self):
        from ImageHorizonLibrary import ImageNotFoundException

        with patch(self._locate, return_value=(0,0)):
            self.assertTrue(self.lib.does_exist('doesentmatter'))

        run_on_failure = MagicMock()
        with patch(self.locate, side_effect=ImageNotFoundException('')), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):
            self.assertFalse(self.lib.does_exist('doesentmatter'))
            self.assertEquals(len(run_on_failure.mock_calls), 0)

    def test_wait_for_happy_path(self):
        from ImageHorizonLibrary import ImageNotFoundException
        run_on_failure = MagicMock()

        with patch(self._locate, return_value=(0,0)), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):
            self.lib.wait_for('doesentmatter', timeout=1)
            self.assertEquals(len(run_on_failure.mock_calls), 0)

    def test_wait_for_negative_path(self):
        from ImageHorizonLibrary import ImageNotFoundException
        run_on_failure = MagicMock()

        with self.assertRaises(ImageNotFoundException), \
             patch(self.locate, side_effect=ImageNotFoundException('')), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):

            start = time.time()
            self.lib.wait_for('notfound', timeout=u'1')
            stop = time.time()

            run_on_failure.assert_called_once_with()
            # check that timeout given as string works and it does not use
            # default timeout
            self.assertLess(stop-start, 10)

    def _verify_path_works(self, image_name, expected):
        self.lib.locate(image_name)
        expected_path = path_join(TESTIMG_DIR, expected)
        self.mock.locateCenterOnScreen.assert_called_once_with(expected_path)
        self.mock.reset_mock()

    def test_locate(self):
        from ImageHorizonLibrary import ImageNotFoundException

        for image_name in ('my_picture.png', 'my picture.png', 'MY PICTURE',
                           'mY_PiCtURe'):
            self._verify_path_works(image_name, 'my_picture.png')

        self.mock.locateCenterOnScreen.return_value = None
        run_on_failure = MagicMock()
        with self.assertRaises(ImageNotFoundException), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):
            self.lib.locate('nonexistent')
            run_on_failure.assert_called_once_with()

    def test_locate_with_valid_reference_folder(self):
        for ref, img in (('reference_images', 'my_picture.png'),
                         (u'./reference_images', 'my picture.png'),
                         ('../../tests/utest/reference_images', 'MY PICTURE')):

            ref = path_join(CURDIR, ref)
            self.lib.reference_folder = ref
            self._verify_path_works(img, 'my_picture.png')

        self.lib.reference_folder = path_join(CURDIR, 'symbolic_link')
        self.lib.locate('mY_PiCtURe')
        expected_path = path_join(CURDIR, 'symbolic_link', 'my_picture.png')
        self.mock.locateCenterOnScreen.assert_called_once_with(expected_path)
        self.mock.reset_mock()

    def test_locate_with_invalid_reference_folder(self):
        from ImageHorizonLibrary import ReferenceFolderException

        for invalid_folder in (None, 123, 'nonexistent', u'nönëxistänt'):
            self.lib.reference_folder = invalid_folder
            with self.assertRaises(ReferenceFolderException):
                self.lib.locate('doesentmatter')

        if not self.lib.is_windows:
            self.lib.reference_folder = TESTIMG_DIR.replace('/', '\\')
            with self.assertRaises(ReferenceFolderException):
                self.lib.locate('doesentmatter')

    def test_locate_with_invalid_image_name(self):
        from ImageHorizonLibrary import InvalidImageException

        for invalid_image_name in (None, 123, 1.2, True, self.lib.__class__()):
            with self.assertRaises(InvalidImageException):
                self.lib.locate(invalid_image_name)
