import pyautogui as ag


class MouseException(Exception):
    pass


class _Mouse(object):

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def click_to_the_above_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''
        Click (offset) abowe a known location.
        Example:
            ${image_location} = locate(my image)
            Click to the abowe of    ${image_location}    50
        '''
        self._click_to_the_direction_of('up', location, offset,
                                        clicks, button, interval)

    def click_to_the_below_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''
        Click (offset) under a known location.
        Example:
            ${image_location} = locate(my image)
            Click to the below of    ${image_location}    50
        '''
        self._click_to_the_direction_of('down', location, offset,
                                        clicks, button, interval)

    def click_to_the_left_of(self, location, offset, clicks=1,
                             button='left', interval=0.0):
        '''
        Click (offset) to the left from known location.
        Example:
            ${image_location} = locate(my image)
            Click to the left of    ${image_location}    50
        '''
        self._click_to_the_direction_of('left', location, offset,
                                        clicks, button, interval)

    def click_to_the_right_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''
        Click (offset) to the right from known location.
        Example:
            ${image_location} = locate(my image)
            Click to the right of    ${image_location}    50
        '''
        self._click_to_the_direction_of('right', location, offset,
                                        clicks, button, interval)

    def move_to(self, *coordinates):
        '''
        Moves the mouse pointer to an absolute location (x, y).
        Takes either a tuple (x, y) or separate values x and y.
        X grows from left to right.
        Y grows from top to bottom.
        Examples:
            Move to    25    150
            Move to    (25, 150)
        '''
        if not len(coordinates) in [1, 2]:
            raise MouseException('Invalid number of coordinates. Please give '
                                 'either (x, y) or x, y.')
        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1])
        ag.moveTo(*coordinates)

    def click(self, button='left'):
        '''
        Clicks the mouse with the specified button.
        '''
        ag.click(button=button)

    def double_click(self, button='left', interval=0.0):
        '''
        Double clicks the mouse with the specified button.
        Argument interval specifies the time between clicks.
        '''
        ag.doubleClick(button=button, interval=float(interval))

    def triple_click(self, button='left', interval=0.0):
        '''
        Triple clicks the mouse with the specified button.
        Argument interval specifies the time between clicks.
        '''
        ag.tripleClick(button=button, interval=float(interval))

