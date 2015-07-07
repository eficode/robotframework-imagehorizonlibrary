import pyautogui as ag


class MouseException(Exception):
    pass


class _Mouse(object):

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def click_to_the_above_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        self._click_to_the_direction_of(self, 'up', location, offset,
                                        clicks, button, interval)

    def click_to_the_below_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        self._click_to_the_direction_of(self, 'down', location, offset,
                                        clicks, button, interval)

    def click_to_the_left_of(self, location, offset, clicks=1,
                             button='left', interval=0.0):
        self._click_to_the_direction_of(self, 'left', location, offset,
                                        clicks, button, interval)

    def click_to_the_right_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        self._click_to_the_direction_of(self, 'right', location, offset,
                                        clicks, button, interval)

    def move_to(self, *coordinates):
        if not len(coordinates) in [1, 2]:
            raise MouseException('Invalid number of coordinates. Please give '
                                 'either (x, y) or x, y.')
        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1])
        ag.moveTo(*coordinates)

    def click(self, button='left'):
        ag.click(button=button)

    def double_click(self, button='left', interval=0.0):
        ag.doubleClick(button=button, interval=float(interval))

    def triple_click(self, button='left', interval=0.0):
        ag.tripleClick(button=button, interval=float(interval))

