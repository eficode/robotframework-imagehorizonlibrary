class ImageHorizonLibraryException(Exception):
    pass

class KeyboardException(Exception):
    pass


try:
    import pyautogui as ag
except ImportError:
    raise ImageHorizonLibraryException('Please install pyautogui')

try:
    import robot
except ImportError:
    raise ImageHorizonLibraryException('Please install Robot Framework')

import utils
from interaction import *
from recognition import *

class ImageHorizonLibrary(_Keyboard,
                          _Mouse,
                          _OperatingSystem,
                          _RecognizeImages,
                          _Screenshot):

    def __init__(self, reference_folder=None, screenshot_folder=None,
                 keyword_on_failure='ImageHorizonLibrary.Take A Screenshot'):
        self.reference_folder = reference_folder
        self.screenshot_folder = screenshot_folder
        self.keyword_on_failure = keyword_on_failure
        self.open_applications = {}
        self.screenshot_counter = 1
        self.is_windows = utils.is_windows()
        self.is_mac = utils.is_mac()
        self.is_linux = utils.is_linux()
        if utils.is_java():
            raise ImageHorizonLibraryException('Java is not supported.'
                                               ' Please use pybot.')

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        x, y = location
        offset = int(offset)
        if direction == 'left':
            x = x - offset
        if direction == 'up':
            y = y - offset
        if direction == 'right':
            x = x + offset
        if direction == 'down':
            y = y + offset
        ag.click(x, y, clicks=clicks, button=button, interval=interval)

    def _convert_to_valid_special_key(self, key):
        key = key.lower()
        if key.startswith('key.'):
            key = key.split('key.', 1)[1]
        elif len(key) > 1:
            return None
        if key in ag.KEYBOARD_KEYS:
            return key
        return None

    def _validate_keys(self, keys, fail_fast=True):
        valid_keys = []
        for key in keys:
            key = self._convert_to_valid_special_key(key)
            if not key:
                raise KeyboardException('Invalid keyboard key "%s", valid '
                                        'keyboard keys are:\n%r' %
                                        (key, ', '.join(ag.KEYBOARD_KEYS)))
            valid_keys.append(key)
        return valid_keys

    def _press(self, *keys, **options):
        keys = self._validate_keys(keys)
        ag.hotkey(*keys, **options)