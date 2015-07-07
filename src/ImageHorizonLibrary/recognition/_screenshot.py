from os.path import abspath, join as path_join
from random import choice
from string import ascii_lowercase

import pyautogui as ag
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class _Screenshot(object):

    def _make_up_filename(self):
        try:
            path = BuiltIn().get_variable_value('${SUITE NAME}')
            path = '%s-screenshot' % path.replace(' ', '')
        except RobotNotRunningError:
            rand_str = ''.join(choice(ascii_lowercase) for _ in range(7))
            path = 'ImageHorizon-%s-screenshot' % rand_str
        return '%s-%d.png' % (path, self.screenshot_counter)

    def take_a_screenshot(self):
        target_dir = self.screenshot_folder if self.screenshot_folder else ''
        path = self._make_up_filename()
        path = abspath(path_join(target_dir, path))
        ag.screenshot(path)

