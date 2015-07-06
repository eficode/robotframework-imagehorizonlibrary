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

    def _locate(self, reference_image):
        reference_image = self.__normalize(reference_image)
        location = ag.locateCenterOnScreen(reference_image)
        if location == None:
            raise ImageNotFoundException('Reference image "%s" was not found '
                                         'on screen' % reference_image)
        return location

    def click_image(self, image_name):
        center_location = self._locate(image_name)
        logger.info('Clicking image "%s" in position %s' % (image_name,
                                                            center_location))
        ag.click(center_location)
        return center_location

    def wait_for(self, image_name, timeout=10):
        image_name = self.__normalize(image_name)
        stop_time = time() + int(timeout)
        while time() < stop_time:
            try:
                location = self._locate(image_name)
            except ImageNotFoundException:
                pass
            else:
                return location
        raise ImageNotFoundException('Reference image "%s" was not found '
                                     'on screen' % image_name)







