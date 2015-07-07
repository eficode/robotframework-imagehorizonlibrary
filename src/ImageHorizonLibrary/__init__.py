class ImageHorizonLibraryException(Exception):
    pass

try:
    import pyautogui
except ImportError:
    raise ImageHorizonLibraryException('Please install pyautogui')

try:
    import robot
except ImportError:
    raise ImageHorizonLibraryException('Please install Robot Framework')

import utils
from interaction import *
from recognition import *

class ImageHorizonLibrary(_RecognizeImages, 
	  					  _Keyboard,
                          _Mouse,
	  					  _OperatingSystem):
    def __init__(self, reference_folder=None):
        self.reference_folder = reference_folder
        self.open_applications = {}
        self.is_windows = utils.is_windows()
        self.is_mac = utils.is_mac()
        self.is_linux = utils.is_linux()
        if utils.is_java():
            raise ImageHorizonLibraryException('Java is not supported.'
                                               ' Please use pybot.')
