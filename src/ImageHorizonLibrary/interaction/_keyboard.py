import pyautogui as ag

class _Keyboard(object):

    def type(self, *keys_or_text, **options):
        for key_or_text in keys_or_text:
            key = self._convert_to_valid_special_key(key_or_text)
            if key:
                ag.press(key, **options)
            else:
                ag.typewrite(key_or_text, **options)

    def type_with_keys_down(self, text, *keys, **options):
        pause = float(options.get('pause', 0.0))
        interval = float(options.get('interval', 0.0))
        valid_keys = self._validate_keys(keys)
        for key in valid_keys:
            ag.keyDown(key, pause=pause)
        ag.typewrite(text, pause=pause, interval=interval)
        for key in valid_keys:
            ag.keyUp(key, pause=pause)

    def press_combination(self, *keys, **options):
        self._press(*keys, **options)
