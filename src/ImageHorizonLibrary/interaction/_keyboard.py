import pyautogui as ag

class KeyboardException(Exception):
    pass

class _Keyboard(object):

    def __convert_to_valid_special_key(self, key):
        key = key.lower()
        if not key.startswith('key.'):
            return None
        key = key.split('key.', 1)[1]
        if key in ag.KEYBOARD_KEYS:
            return key
        return None

    def __normalize(self, keys, fail_fast=True):
        valid_keys = []
        for key in keys:
            key = self.__convert_to_valid_special_key(key)
            if not key:
                raise KeyboardException('Invalid keyboard key "%s", valid '
                                        'keyboard keys are:\n %s' %
                                        (key, ', '.join(ag.KEYBOARD_KEYS)))
            valid_keys.append(key)
        return valid_keys


    def press(self, *keys):
        keys = self.__normalize(keys)
        ag.hotkey(*keys)

    def type(self, *keys_or_text, **options):
        for key_or_text in keys_or_text:
            key = self.__convert_to_valid_special_key(key_or_text)
            if key:
                ag.press(key, **options)
            else:
                ag.typewrite(key_or_text, **options)
