from unittest import TestCase
from mock import patch, MagicMock

import pyautogui

class TestKeyboard(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.KEYBOARD_KEYS = pyautogui.KEYBOARD_KEYS
        self.patcher = patch.dict('sys.modules', {'pyautogui' : self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        self.mock.reset_mock()
        self.patcher.stop()

    def test_type_with_text(self):
        self.lib.type('hey you fool')
        self.mock.typewrite.assert_called_once_with('hey you fool')

    def test_type_with_text_and_keys(self):
        self.lib.type('I love you', 'Key.ENTER')
        self.mock.typewrite.assert_called_once_with('I love you')
        self.mock.press.assert_called_once_with('enter')

    def test_type_with_keys_down(self):
        self.lib.type_with_keys_down('hello', 'key.shift')
        self.mock.keyDown.assert_called_once_with('shift', pause=0.0)
        self.mock.typewrite.assert_called_once_with('hello', pause=0.0,
                                                    interval=0.0)
        self.mock.keyUp.assert_called_once_with('shift', pause=0.0)

    def test_press_combination(self):
        from ImageHorizonLibrary import ImageHorizonLibrary
        with patch('ImageHorizonLibrary.ImageHorizonLibrary._press',
                   autospec=True) as press_mock:
            lib = ImageHorizonLibrary()
            lib.press_combination('Key.ctrl', 'A')
            press_mock.assert_called_once_with(lib, 'Key.ctrl', 'A')

