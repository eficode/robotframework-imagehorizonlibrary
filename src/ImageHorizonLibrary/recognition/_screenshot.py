from os.path import abspath, join as path_join
from random import choice
from string import ascii_lowercase

import pyautogui as ag
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api import logger as LOGGER

from ..errors import ScreenshotFolderException

class _Screenshot(object):
    def _make_up_filename(self):
        try:
            path = BuiltIn().get_variable_value('${SUITE NAME}')
            path = '%s-screenshot' % path.replace(' ', '')
        except RobotNotRunningError:
            LOGGER.info('Could not get suite name, using default naming scheme')
            path = 'ImageHorizon-screenshot'
        path = '%s-%d.png' % (path, self.screenshot_counter)
        self.screenshot_counter += 1
        return path

    def take_a_screenshot(self):
        target_dir = self.screenshot_folder if self.screenshot_folder else ''
        if not isinstance(target_dir, basestring):
            raise ScreenshotFolderException('Screenshot folder is invalid: '
                                            '"%s"' % target_dir)
        path = self._make_up_filename()
        path = abspath(path_join(target_dir, path))
        LOGGER.info('Screenshot taken: {0}<br/><img src="{0}" '
                    'width="100%" />'.format(path), html=True)
        ag.screenshot(path)

