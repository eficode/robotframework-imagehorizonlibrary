class _Shared(object):
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