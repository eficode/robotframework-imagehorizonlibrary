from time import time
from os.path import abspath, isdir, isfile, join as path_join

import pyautogui as ag
from robot.api import logger


class ImageNotFoundException(Exception):
    pass

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
            raise ImageNotFoundException('Reference image "%s" does not exist'
                                         % path)
        return path

    def click_image(self, image_name):
        center_location = self.locate(image_name)
        logger.info('Clicking image "%s" in position %s' % (image_name,
                                                            center_location))
        ag.click(center_location)
        return center_location

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

    def does_exist(self, reference_image):
        try:
            return bool(self.locate(reference_image))
        except ImageNotFoundException:
            return False

    def locate(self, reference_image):
        reference_image = self.__normalize(reference_image)
        location = ag.locateCenterOnScreen(reference_image)
        if location == None:
            raise ImageNotFoundException('Reference image "%s" was not found '
                                         'on screen' % reference_image)
        return location

    def wait_for(self, image_name, timeout=10):
        image_name = self.__normalize(image_name)
        stop_time = time() + int(timeout)
        while time() < stop_time:
            try:
                location = self.locate(image_name)
                break
            except ImageNotFoundException:
                raise
        logger.info('Found image "%s" in position %s' % (image_name, location))
        return location







