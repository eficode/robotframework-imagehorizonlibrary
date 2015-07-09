import time

from unittest import TestCase
from os.path import abspath, dirname, join as path_join
from mock import call, MagicMock, patch

TESTIMG_DIR = path_join(abspath(dirname(__file__)), 'reference_images')

class TestRecognizeImages(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.patcher = patch.dict('sys.modules', {'pyautogui' : self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary(reference_folder=TESTIMG_DIR)
        self.locate = 'ImageHorizonLibrary.ImageHorizonLibrary.locate'

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

        with patch(self.locate, return_value=(0,0)):
            self.assertTrue(self.lib.does_exist('doesentmatter'))

        run_on_failure = MagicMock()
        with patch(self.locate, side_effect=ImageNotFoundException('')), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):
            self.assertFalse(self.lib.does_exist('doesentmatter'))
            self.assertEquals(len(run_on_failure.mock_calls), 0)

    def test_happy_path_wait_for(self):
        from ImageHorizonLibrary import ImageNotFoundException
        run_on_failure = MagicMock()

        with patch(self.locate, return_value=(0,0)), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):
            self.lib.wait_for('doesentmatter', timeout=1)
            self.assertEquals(len(run_on_failure.mock_calls), 0)

    def test_negative_path_wait_for(self):
        from ImageHorizonLibrary import ImageNotFoundException
        run_on_failure = MagicMock()

        with self.assertRaises(ImageNotFoundException), \
             patch(self.locate, side_effect=ImageNotFoundException('')), \
             patch.object(self.lib, '_run_on_failure', run_on_failure):

            start = time.time()
            self.lib.wait_for('doesentmatter', timeout=u'1')
            stop = time.time()

            run_on_failure.assert_called_once_with()
            # check that timeout given as string works and it does not use
            # default timeout
            self.assertLess(stop-start, 10)