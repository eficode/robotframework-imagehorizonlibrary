# -*- coding: utf-8 -*-
import pyautogui as ag

from ..errors import MouseException


class _Mouse(object):

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def click_to_the_above_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks above of given location by given offset.

        ``location`` can be any Python sequence type (tuple, list, etc.) that
        represents coordinates on the screen ie. have an x-value and y-value.
        Locating-related keywords return location you can use with this
        keyword.

        ``offset`` is the number of pixels from the specified ``location``.

        ``clicks`` is how many times the mouse button is clicked.

        See `Click` for documentation for valid buttons.

        Example:

        | ${image location}=    | Locate             | my image |        |
        | Click To The Above Of | ${image location}  | 50       |        |
        | @{coordinates}=       | Create List        | ${600}   | ${500} |
        | Click To The Above Of | ${coordinates}     | 100      |        |
        '''
        self._click_to_the_direction_of('up', location, offset,
                                        clicks, button, interval)

    def click_to_the_below_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks below of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('down', location, offset,
                                        clicks, button, interval)

    def click_to_the_left_of(self, location, offset, clicks=1,
                             button='left', interval=0.0):
        '''Clicks left of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('left', location, offset,
                                        clicks, button, interval)

    def click_to_the_right_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks right of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('right', location, offset,
                                        clicks, button, interval)

    def move_to(self, *coordinates):
        '''Moves the mouse pointer to an absolute coordinates.

        ``coordinates`` can either be a Python sequence type with two values
        (eg. ``(x, y)``) or separate values ``x`` and ``y``:

        | Move To         | 25             | 150       |     |
        | @{coordinates}= | Create List    | 25        | 150 |
        | Move To         | ${coordinates} |           |     |
        | ${coords}=      | Evaluate       | (25, 150) |     |
        | Move To         | ${coords}      |           |     |


        X grows from left to right and Y grows from top to bottom, which means
        that top left corner of the screen is (0, 0)
        '''
        if len(coordinates) > 2 or (len(coordinates) == 1 and
                                    type(coordinates[0]) not in (list, tuple)):
            raise MouseException('Invalid number of coordinates. Please give '
                                 'either (x, y) or x, y.')
        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1])
        else:
            coordinates = coordinates[0]
        try:
            coordinates = [int(coord) for coord in coordinates]
        except ValueError:
            raise MouseException('Coordinates %s are not integers' %
                                 (coordinates,))
        ag.moveTo(*coordinates)

    def mouse_down(self, button='left'):
        '''Presses specidied mouse button down'''
        ag.mouseDown(button=button)

    def mouse_up(self, button='left'):
        '''Releases specified mouse button'''
        ag.mouseUp(button=button)

    def click(self, button='left'):
        '''Clicks with the specified mouse button.

        Valid buttons are ``left``, ``right`` or ``middle``.
        '''
        ag.click(button=button)

    def double_click(self, button='left', interval=0.0):
        '''Double clicks with the specified mouse button.

        See documentation of ``button`` in `Click`.

        ``interval`` specifies the time between clicks and should be
        floating point number.
        '''
        ag.doubleClick(button=button, interval=float(interval))

    def triple_click(self, button='left', interval=0.0):
        '''Triple clicks with the specified mouse button.

        See documentation of ``button`` in `Click`.

        See documentation of ``interval`` in `Double Click`.
        '''
        ag.tripleClick(button=button, interval=float(interval))
