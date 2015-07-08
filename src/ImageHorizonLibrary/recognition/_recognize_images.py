from os.path import abspath, isdir, isfile, join as path_join
from time import time
from contextlib import contextmanager

import pyautogui as ag
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class ImageNotFoundException(Exception):
    
    def __init__(self, image_name):
        self.image_name = image_name

    def __str__(self):
        return 'Reference image "%s" was not found on screen' % self.image_name

class ReferenceFolderException(Exception):
    pass


class _RecognizeImages(object):

    def __normalize(self, path):
        if (not self.reference_folder or
            not isinstance(self.reference_folder, basestring) or
            not isdir(self.reference_folder)):
            raise ReferenceFolderException('Reference folder is invalid: "%s"'
                                           % self.reference_folder)
        path = path.replace(' ', '_').lower()
        if not path.endswith('.png'):
            path += '.png'
        path = abspath(path_join(self.reference_folder, path))
        if not isfile(path):
            raise ImageNotFoundException(path)
        return path

    def click_image(self, image_name):
        center_location = self.locate(image_name)
        logger.info('Clicking image "%s" in position %s' % (image_name,
                                                            center_location))
        ag.click(center_location)
        return center_location

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def _locate_and_click_direction(self, direction, reference_image, offset,
                                    clicks, button, interval):
        location = self.locate(reference_image)
        self._click_to_the_direction_of(self, direction, location, offset,
                                        clicks, button, interval)

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


    def does_exist(self, reference_image):
        with self._suppress_keyword_on_failure():
            try:
                return bool(self.locate(reference_image))
            except ImageNotFoundException:
                return False

    def _run_on_failure(self):
        if not self.keyword_on_failure:
            return
        try:
            BuiltIn().run_keyword(self.keyword_on_failure)
        except:
            logger.warn('Failed to take a screenshot. '
                        'Is Robot Framework running?')

    def locate(self, reference_image):
        reference_image = self.__normalize(reference_image)
        location = ag.locateCenterOnScreen(reference_image)
        if location == None:
            self._run_on_failure()
            raise ImageNotFoundException(reference_image)
        return location

    def wait_for(self, reference_image, timeout=10):
        stop_time = time() + int(timeout)
        location = None
        with self._suppress_keyword_on_failure():
            while time() < stop_time:
                try:
                    location = self.locate(reference_image)
                    break
                except ImageNotFoundException:
                    pass
        if location == None:
            self._run_on_failure()
            raise ImageNotFoundException(reference_image)
        logger.info('Found image "%s" in position %s' % (reference_image, 
                                                         location))
        return location







