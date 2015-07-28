# -*- coding: utf-8 -*-
from os.path import abspath, isdir, isfile, join as path_join
from time import time
from contextlib import contextmanager

import pyautogui as ag
from robot.api import logger as LOGGER

from ..errors import ImageNotFoundException, InvalidImageException
from ..errors import ReferenceFolderException


class _RecognizeImages(object):

    def __normalize(self, path):
        if (not self.reference_folder or
            not isinstance(self.reference_folder, basestring) or
            not isdir(self.reference_folder)):
            raise ReferenceFolderException('Reference folder is invalid: "%s"'
                                           % self.reference_folder)
        if (not path or not isinstance(path, basestring)):
            raise InvalidImageException('"%s" is invalid image name.' % path)
        path = path.lower().replace(' ', '_')
        if not path.endswith('.png'):
            path += '.png'
        path = abspath(path_join(self.reference_folder, path))
        if not isfile(path):
            raise ImageNotFoundException(path)
        return path

    def click_image(self, image_name):
        center_location = self.locate(image_name)
        LOGGER.info('Clicking image "%s" in position %s' % (image_name,
                                                            center_location))
        ag.click(center_location)
        return center_location

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def _locate_and_click_direction(self, direction, reference_image, offset,
                                    clicks, button, interval):
        location = self.locate(reference_image)
        self._click_to_the_direction_of(direction, location, offset, clicks,
                                        button, interval)

    def click_to_the_above_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0):
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_below_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0):
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_left_of_image(self, reference_image, offset, clicks=1,
                                   button='left', interval=0.0):
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_right_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0):
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks, button, interval)

    def copy_from_the_above_of(self, reference_image, offset):
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_below_of(self, reference_image, offset):
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_left_of(self, reference_image, offset):
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_right_of(self, reference_image, offset):
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    @contextmanager
    def _suppress_keyword_on_failure(self):
        keyword = self.keyword_on_failure
        self.keyword_on_failure = None
        yield None
        self.keyword_on_failure = keyword

    def _locate(self, reference_image, log_it=True):
        reference_image = str(self.__normalize(reference_image))
        location = ag.locateCenterOnScreen(reference_image)
        if location == None:
            if log_it:
                LOGGER.info('Image "%s" was not found '
                            'on screen.' % reference_image)
            self._run_on_failure()
            raise ImageNotFoundException(reference_image)
        if log_it:
            LOGGER.info('Image "%s" found at %r' % (reference_image, location))
        return location

    def does_exist(self, reference_image):
        with self._suppress_keyword_on_failure():
            try:
                return bool(self._locate(reference_image, log_it=False))
            except ImageNotFoundException:
                return False

    def locate(self, reference_image):
        return self._locate(reference_image)

    def wait_for(self, reference_image, timeout=10):
        stop_time = time() + int(timeout)
        location = None
        with self._suppress_keyword_on_failure():
            while time() < stop_time:
                try:
                    location = self._locate(reference_image, log_it=False)
                    break
                except ImageNotFoundException:
                    pass
        if location == None:
            self._run_on_failure()
            raise ImageNotFoundException(reference_image)
        LOGGER.info('Image "%s" found at %r' % (reference_image, location))
        return location
