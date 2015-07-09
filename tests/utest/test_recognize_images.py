from unittest import TestCase

from mock import Mock, patch

class TestRecognizeImages(TestCase):
    def setUp(self):
        self.patcher = patch.dict('sys.modules', {'pyautogui' : MagicMock()})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        self.patcher.stop()

