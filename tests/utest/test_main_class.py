from unittest import TestCase

from mock import MagicMock, patch

class TestMainClass(TestCase):
    def setUp(self):
        self.pyautogui_mock = MagicMock()
        self.Tk_mock = MagicMock()
        self.clipboard_mock = MagicMock()
        self.clipboard_mock.clipboard_get.return_value = 'copied text'
        self.Tk_mock.Tk.return_value = self.clipboard_mock
        self.patcher = patch.dict('sys.modules',
                                  {'pyautogui' : self.pyautogui_mock,
                                   'Tkinter' : self.Tk_mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        for mock in (self.Tk_mock, self.clipboard_mock, self.pyautogui_mock):
            mock.reset_mock()
        self.patcher.stop()

    def test_copy(self):
        from ImageHorizonLibrary import ImageHorizonLibrary

        with patch.object(ImageHorizonLibrary, '_press') as press_mock:
             retval = self.lib.copy()
             self.assertEquals(retval, 'copied text')
             self.clipboard_mock.clipboard_get.assert_called_once_with()
             press_mock.assert_called_once_with('Key.command', 'c')

             press_mock.reset_mock()
             self.clipboard_mock.reset_mock()

             self.lib.is_mac = False
             retval = self.lib.copy()
             self.assertEquals(retval, 'copied text')
             self.clipboard_mock.clipboard_get.assert_called_once_with()
             press_mock.assert_called_once_with('Key.ctrl', 'c')

    def test_alert(self):
        self.lib.pause()
        self.pyautogui_mock.alert.assert_any_calls()

