# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch, MagicMock

import pyautogui


class TestKeyboard(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.KEYBOARD_KEYS = pyautogui.KEYBOARD_KEYS
        self.patcher = patch.dict('sys.modules', {'pyautogui': self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        self.mock.reset_mock()
        self.patcher.stop()

    def test_type_with_text(self):
        self.lib.type('hey you fool')
        self.mock.typewrite.assert_called_once_with('hey you fool')
        self.mock.reset_mock()

        self.lib.type('.')
        self.mock.press.assert_called_once_with('.')

    def test_type_with_umlauts(self):
        self.lib.type(u'öäöäü')
        self.mock.typewrite.assert_called_once_with(u'öäöäü')

    def test_type_with_text_and_keys(self):
        self.lib.type('I love you', 'Key.ENTER')
        self.mock.typewrite.assert_called_once_with('I love you')
        self.mock.press.assert_called_once_with('enter')

    def test_type_with_utf8_keys(self):
        self.lib.type(u'key.Tab')
        self.assertEquals(self.mock.typewrite.call_count, 0)
        self.mock.press.assert_called_once_with('tab')
        self.assertEquals(type(self.mock.press.call_args[0][0]),
                          type(str()))

    def test_type_with_keys_down(self):
        self.lib.type_with_keys_down('hello', 'key.shift')
        self.mock.keyDown.assert_called_once_with('shift')
        self.mock.typewrite.assert_called_once_with('hello')
        self.mock.keyUp.assert_called_once_with('shift')

    def test_type_with_keys_down_with_invalid_keys(self):
        from ImageHorizonLibrary import KeyboardException

        expected_msg = ', '.join(self.mock.KEYBOARD_KEYS)

        with self.assertRaises(KeyboardException) as e:
            self.lib.type_with_keys_down('sometext', 'enter')
            self.assertTrue(e.message.endswith(expected_msg))

        with self.assertRaises(KeyboardException) as e:
            self.lib.type_with_keys_down('sometext', 'enter')
            self.assertTrue(e.message.endswith(expected_msg))

    def test_press_combination(self):
            self.lib.press_combination('Key.ctrl', 'A')
            self.mock.hotkey.assert_called_once_with('ctrl', 'a')
            self.mock.reset_mock()

            for key in self.mock.KEYBOARD_KEYS:
                self.lib.press_combination('Key.%s' % key)
                self.mock.hotkey.assert_called_once_with(key.lower())
                self.mock.reset_mock()
