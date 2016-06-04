# -*- coding: utf-8 -*-
from os import listdir
from os.path import abspath, isdir, isfile, join as path_join
from time import time
from contextlib import contextmanager

import pyautogui as ag
from robot.api import logger as LOGGER

from ImageHorizonLibrary.errors import ImageNotFoundException, InvalidImageException
from ImageHorizonLibrary.errors import ReferenceFolderException


class _RecognizeImages(object):
    def __init__(self):
        self.reference_folder = 'c:\\robot'

    def __normalize(self, path):
        if (not self.reference_folder or
                not isinstance(self.reference_folder, basestring) or
                not isdir(self.reference_folder)):
            raise ReferenceFolderException('Reference folder is invalid: '
                                           '"%s"' % self.reference_folder)
        if (not path or not isinstance(path, basestring)):
            raise InvalidImageException('"%s" is invalid image name.' % path)
        path = unicode(path.lower().replace(' ', '_'))
        path = abspath(path_join(self.reference_folder, path))
        if not path.endswith('.png') and not isdir(path):
            path += '.png'
        if not isfile(path) and not isdir(path):
            raise InvalidImageException('Image path not found: "%s".' % path)
        return path

    def click_image(self, reference_image):
        '''Finds the reference image on screen and clicks it once.

        ``reference_image`` is automatically normalized as described in the
        `Reference image names`.
        '''
        center_location = self.locate(reference_image=reference_image)
        LOGGER.info('Clicking image "%s" in position %s' % (reference_image,
                                                            center_location))
        ag.click(center_location)
        return center_location

    def click_image_in_image(self, reference_image, contain_image):
        '''Finds the reference image in the contain image and clicks it once.

        ``reference_image`` and ``contain_image`` are automatically normalized as described in the
        `Reference image names`.
        '''
        contain_img_location = self._locate(reference_image=contain_image, get_center=False)
        img_in_img_location = self._locate(reference_image=reference_image, contain_image=contain_image)

        x_to_click = contain_img_location[0] + img_in_img_location[0] + img_in_img_location[2]/2
        y_to_click = contain_img_location[1] + img_in_img_location[1] + img_in_img_location[3]/2
        LOGGER.info('Clicking image "{img}" in position ({x}, {y})'.format(img=reference_image,
                                                                           x=x_to_click, y=y_to_click))
        ag.click(x=x_to_click, y=y_to_click)
        return img_in_img_location

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
        '''Clicks above of reference image by given offset.

        See `Reference image names` for documentation for ``reference_image``.

        ``offset`` is the number of pixels from the center of the reference
        image.

        ``clicks`` and ``button`` are documented in `Click To The Above Of`.
        '''
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_below_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0):
        '''Clicks below of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_left_of_image(self, reference_image, offset, clicks=1,
                                   button='left', interval=0.0):
        '''Clicks left of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks, button, interval)

    def click_to_the_right_of_image(self, reference_image, offset, clicks=1,
                                    button='left', interval=0.0):
        '''Clicks right of reference image by given offset.

        See argument documentation in `Click To The Above Of Image`.
        '''
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks, button, interval)

    def copy_from_the_above_of(self, reference_image, offset):
        '''Clicks three times above of reference image by given offset and
        copies.

        See `Reference image names` for documentation for ``reference_image``.

        See `Click To The Above Of Image` for documentation for ``offset``.

        Copy is done by pressing ``Ctrl+C`` on Windows and Linux and ``⌘+C``
        on OS X.
        '''
        self._locate_and_click_direction('up', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_below_of(self, reference_image, offset):
        '''Clicks three times below of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('down', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_left_of(self, reference_image, offset):
        '''Clicks three times left of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('left', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    def copy_from_the_right_of(self, reference_image, offset):
        '''Clicks three times right of reference image by given offset and
        copies.

        See argument documentation in `Copy From The Above Of`.
        '''
        self._locate_and_click_direction('right', reference_image, offset,
                                         clicks=3, button='left', interval=0.0)
        return self.copy()

    @contextmanager
    def _suppress_keyword_on_failure(self):
        keyword = self.keyword_on_failure
        self.keyword_on_failure = None
        yield None
        self.keyword_on_failure = keyword

    def _locate(self, reference_image, contain_image=None, get_center=True, log_it=True):
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

        def calculate_center(position):
            return position[0]/2, position[1]/2, position[2], position[3]

        def try_locate(ref_image):
            location = None
            with self._suppress_keyword_on_failure():
                try:
                    if contain_image is None:
                        # returns (x, y)
                        location = ag.locateCenterOnScreen(ref_image.encode('utf-8')) if get_center \
                            else ag.locateOnScreen(ref_image.encode('utf-8'))
                    else:
                        # returns (x, y, w, h)
                        location = calculate_center(ag.locate(
                            ref_image.encode('utf-8'), contain_image.encode('utf-8'))) if get_center \
                            else ag.locate(ref_image.encode('utf-8'), contain_image.encode('utf-8'))
                except ImageNotFoundException:
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
        return location

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

    def locate(self, reference_image, get_center=True):
        '''Locate image on screen. If ``get_center`` is set to ``False``

        Fails if image is not found on screen.

        Returns Python tuple ``(x, y)`` coordinates of the center of the first found instance of the image on the
        screen. If ``get_center`` is set to ``False``, will returns Python tuple ``(left, top, width, height)``
        coordinate of first found instance of the image on the screen
        '''
        return self._locate(reference_image=reference_image, get_center=get_center)

    def wait_for(self, reference_image, timeout=10):
        '''Tries to locate given image from the screen for given time.

        Fail if the image is not found on the screen after ``timeout`` has
        expired.

        See `Reference image names` for documentation for ``reference_image``.

        ``timeout`` is given in seconds.

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
