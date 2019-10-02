# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch, MagicMock


KEYBOARD_KEYS = [
    '\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert',
    'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    'shift', 'shiftleft', 'shiftright', 'sleep', 'stop', 'subtract', 'tab',
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright',
    'yen', 'command', 'option', 'optionleft'
]

class TestKeyboard(TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.KEYBOARD_KEYS = KEYBOARD_KEYS
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
        self.lib.type('öäöäü')
        self.mock.typewrite.assert_called_once_with('öäöäü')

    def test_type_with_text_and_keys(self):
        self.lib.type('I love you', 'Key.ENTER')
        self.mock.typewrite.assert_called_once_with('I love you')
        self.mock.press.assert_called_once_with('enter')

    def test_type_with_utf8_keys(self):
        self.lib.type('key.Tab')
        self.assertEqual(self.mock.typewrite.call_count, 0)
        self.mock.press.assert_called_once_with('tab')
        self.assertEqual(type(self.mock.press.call_args[0][0]),
                          type(str()))

    def test_type_with_keys_down(self):
        self.lib.type_with_keys_down('hello', 'key.shift')
        self.mock.keyDown.assert_called_once_with('shift')
        self.mock.typewrite.assert_called_once_with('hello')
        self.mock.keyUp.assert_called_once_with('shift')

    def test_type_with_keys_down_with_invalid_keys(self):
        from ImageHorizonLibrary import KeyboardException

        expected_msg = ('Invalid keyboard key "enter", valid keyboard keys '
                        'are:\n%r' % ', '.join(self.mock.KEYBOARD_KEYS))
        with self.assertRaises(KeyboardException) as cm:
            self.lib.type_with_keys_down('sometext', 'enter')
        self.assertEqual(str(cm.exception), expected_msg)

    def test_press_combination(self):
            self.lib.press_combination('Key.ctrl', 'A')
            self.mock.hotkey.assert_called_once_with('ctrl', 'a')
            self.mock.reset_mock()

            for key in self.mock.KEYBOARD_KEYS:
                self.lib.press_combination('Key.%s' % key)
                self.mock.hotkey.assert_called_once_with(key.lower())
                self.mock.reset_mock()
