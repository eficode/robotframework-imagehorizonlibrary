# -*- coding: utf-8 -*-
import pyautogui as ag


class _Keyboard(object):
    def press_combination(self, *keys):
        '''Press given keyboard keys.

        All keyboard keys must be prefixed with ``Key.``.

        Keyboard keys are case-insensitive:

        | Press Combination | KEY.ALT | key.f4 | 
        | Press Combination | kEy.EnD |        |

        [https://pyautogui.readthedocs.org/en/latest/keyboard.html#keyboard-keys|
        See valid keyboard keys here].
        '''
        self._press(*keys)

    def type(self, *keys_or_text):
        '''Type text and keyboard keys.

        See valid keyboard keys in `Press Combination`.

        Examples:

        | Type | separated              | Key.ENTER | by linebreak |
        | Type | Submit this with enter | Key.enter |              |
        | Type | key.windows            | notepad   | Key.enter    |
        '''
        for key_or_text in keys_or_text:
            key = self._convert_to_valid_special_key(key_or_text)
            if key:
                ag.press(key)
            else:
                ag.typewrite(key_or_text)


    def type_with_keys_down(self, text, *keys):
        '''Press keyboard keys down, then write given text, then release the
        keyboard keys.

        See valid keyboard keys in `Press Combination`.

        Examples:

        | Type with keys down | write this in caps  | Key.Shift |
        '''
        valid_keys = self._validate_keys(keys)
        for key in valid_keys:
            ag.keyDown(key)
        ag.typewrite(text)
        for key in valid_keys:
            ag.keyUp(key)
