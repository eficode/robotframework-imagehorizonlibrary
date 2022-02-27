# -*- coding: utf-8 -*-
from os import listdir
from os.path import abspath, isdir, isfile, join as path_join
from time import time
from contextlib import contextmanager

import pyautogui as ag
from robot.api import logger as LOGGER

from ..errors import ImageNotFoundException, InvalidImageException
from ..errors import ReferenceFolderException

class _RecognizeImages(object):

    dflt_timeout = 0

    def __normalize(self, path):
        if (not self.reference_folder or
                not isinstance(self.reference_folder, str) or
                not isdir(self.reference_folder)):
            raise ReferenceFolderException('Reference folder is invalid: '
                                           '"%s"' % self.reference_folder)
        if (not path or not isinstance(path, str)):
            raise InvalidImageException('"%s" is invalid image name.' % path)
        path = str(path.lower().replace(' ', '_'))
        path = abspath(path_join(self.reference_folder, path))
        if not path.endswith('.png') and not isdir(path):
            path += '.png'
        if not isfile(path) and not isdir(path):
            raise InvalidImageException('Image path not found: "%s".' % path)
        return path

    def click_image(self, reference_image, timeout=dflt_timeout):
        '''Finds the reference image on screen and clicks it's center point once.

        ``reference_image`` is automatically normalized as described in the
        `Reference image names`.

        ``timeout`` optional value, in whole seconds. default is 0
        '''
        center_location = self.wait_for(reference_image, timeout)
        LOGGER.info('Clicking image "%s" in position %s' % (reference_image,
                                                            center_location))
        ag.click(center_location)
        return center_location

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def _locate_and_click_direction(self, direction, reference_image, offset,
                                    clicks, button, interval, timeout=dflt_timeout):
        location = self.wait_for(reference_image, timeout)
        self._click_to_the_direction_of(direction, location, offset, clicks,
                                        button, interval)

    def click_to_the_above_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0, timeout=dflt_timeout):
        '''Clicks above of reference image by given offset.

        See `Reference image names` for documentation for ``reference_image``.

        ``offset`` is the number of pixels from the center of the reference
        image.

        ``clicks`` and ``button`` are documented in `Click To The Above Of`.

        ``timeout`` optional value, in whole seconds. default is 0
        '''
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks, button, interval, timeout)

    def click_to_the_below_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0, timeout=dflt_timeout):
        '''Clicks below of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks, button, interval, timeout)

    def click_to_the_left_of_image(self, reference_image, offset, clicks=1,
                                   button='left', interval=0.0, timeout=dflt_timeout):
        '''Clicks left of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks, button, interval, timeout)

    def click_to_the_right_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0, timeout=dflt_timeout):
        '''Clicks right of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks, button, interval, timeout)

    def copy_from_the_above_of(self, reference_image, offset, timeout=dflt_timeout):
        '''Clicks three times above of reference image by given offset and
        copies.

        See `Reference image names` for documentation for ``reference_image``.

        See `Click To The Above Of Image` for documentation for ``offset``.

        Copy is done by pressing ``Ctrl+C`` on Windows and Linux and ``⌘+C``
        on OS X.

        ``timeout`` optional value, in whole seconds. default is 0
        '''
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks=3, button='left', interval=0.0, timeout=timeout)
        return self.copy()

    def copy_from_the_below_of(self, reference_image, offset, timeout=dflt_timeout):
        '''Clicks three times below of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks=3, button='left', interval=0.0, timeout=timeout)
        return self.copy()

    def copy_from_the_left_of(self, reference_image, offset, timeout=dflt_timeout):
        '''Clicks three times left of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks=3, button='left', interval=0.0, timeout=timeout)
        return self.copy()

    def copy_from_the_right_of(self, reference_image, offset, timeout=dflt_timeout):
        '''Clicks three times right of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks=3, button='left', interval=0.0, timeout=timeout)
        return self.copy()

    @contextmanager
    def _suppress_keyword_on_failure(self):
        keyword = self.keyword_on_failure
        self.keyword_on_failure = None
        yield None
        self.keyword_on_failure = keyword

    def _locate(self, reference_image, log_it=True):
        is_dir = False
        try:
            if isdir(self.__normalize(reference_image)):
                is_dir = True
        except InvalidImageException:
            pass
        is_file = False
        try:
            if isfile(self.__normalize(reference_image)):
                is_file = True
        except InvalidImageException:
            pass
        reference_image = self.__normalize(reference_image)

        reference_images = []
        if is_file:
            reference_images = [reference_image]
        elif is_dir:
            for f in listdir(self.__normalize(reference_image)):
                if not isfile(self.__normalize(path_join(reference_image, f))):
                    raise InvalidImageException(
                                            self.__normalize(reference_image))
                reference_images.append(path_join(reference_image, f))

        def try_locate(ref_image):
            location = None
            with self._suppress_keyword_on_failure():
                try:
                    if self.has_cv and self.confidence:
                        location = ag.locateOnScreen(ref_image,
                                                     confidence=self.confidence)
                    else:
                        if self.confidence:
                            LOGGER.warn("Can't set confidence because you don't "
                                        "have OpenCV (python-opencv) installed "
                                        "or a confidence level was not given.")
                        location = ag.locateOnScreen(ref_image)
                except ImageNotFoundException as ex:
                    LOGGER.info(ex)
                    pass
            return location

        location = None
        for ref_image in reference_images:
            location = try_locate(ref_image)
            if location != None:
                break

        if location is None:
            if log_it:
                LOGGER.info('Image "%s" was not found '
                            'on screen.' % reference_image)
            self._run_on_failure()
            raise ImageNotFoundException(reference_image)
        if log_it:
            LOGGER.info('Image "%s" found at %r' % (reference_image, location))
        center_point = ag.center(location)
        x = center_point.x
        y = center_point.y
        if self.has_retina:
            x = x / 2
            y = y / 2
        return (x, y)

    def does_exist(self, reference_image):
        '''Returns ``True`` if reference image was found on screen or
        ``False`` otherwise. Never fails.

        See `Reference image names` for documentation for ``reference_image``.
        '''
        with self._suppress_keyword_on_failure():
            try:
                return bool(self._locate(reference_image, log_it=False))
            except ImageNotFoundException:
                return False

    def locate(self, reference_image):
        '''Locate image on screen.

        Fails if image is not found on screen.

        Returns Python tuple ``(x, y)`` of the coordinates.
        '''
        return self._locate(reference_image)

    def wait_for(self, reference_image, timeout=10):
        '''Tries to locate given image from the screen for given time.

        Fail if the image is not found on the screen after ``timeout`` has
        expired.

        See `Reference image names` for documentation for ``reference_image``.

        ``timeout`` is given in whole seconds.

        Returns Python tuple ``(x, y)`` of the coordinates.
        '''
        stop_time = time() + int(timeout)
        location = None
        with self._suppress_keyword_on_failure():
            while time() < stop_time:
                try:
                    location = self._locate(reference_image, log_it=False)
                    break
                except ImageNotFoundException:
                    pass
        if location is None:
            self._run_on_failure()
            raise ImageNotFoundException(self.__normalize(reference_image))
        LOGGER.info('Image "%s" found at %r' % (reference_image, location))
        return location
