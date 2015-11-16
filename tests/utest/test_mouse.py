# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import call, MagicMock, patch


class TestMouse(TestCase):

    def setUp(self):
        self.mock = MagicMock()
        self.patcher = patch.dict('sys.modules', {'pyautogui': self.mock})
        self.patcher.start()
        from ImageHorizonLibrary import ImageHorizonLibrary, MouseException
        self.lib = ImageHorizonLibrary()

    def tearDown(self):
        self.mock.reset_mock()
        self.patcher.stop()

    def test_all_directional_clicks(self):
        for direction in ['above', 'below', 'left', 'right']:
            fn = getattr(self.lib, 'click_to_the_%s_of' % direction)
            fn((0, 0), '10')
        self.assertEquals(self.mock.click.mock_calls,
                          [call(0, -10, button='left', interval=0.0, clicks=1),
                           call(0, 10, button='left', interval=0.0, clicks=1),
                           call(-10, 0, button='left', interval=0.0, clicks=1),
                           call(10, 0, button='left', interval=0.0, clicks=1)])

    def _verify_directional_clicks_fail(self, direction, kwargs):
        from ImageHorizonLibrary import MouseException

        fn = getattr(self.lib, 'click_to_the_%s_of' % direction)
        with self.assertRaises(MouseException):
            fn((0, 0), 10, **kwargs)
        self.assertEquals(self.mock.click.mock_calls, [])

    def test_arguments_in_directional_clicks(self):
        self.lib.click_to_the_above_of((0, 0), 10, clicks=u'2',
                                       button=u'middle', interval=u'1.2')
        self.assertEquals(self.mock.click.mock_calls, [call(0, -10,
                                                            button='middle',
                                                            interval=1.2,
                                                            clicks=2)])
        self.mock.reset_mock()
        for args in (('below', {'clicks': 'notvalid'}),
                     ('right', {'button': 'notvalid'}),
                     ('left',  {'interval': 'notvalid'})):
            self._verify_directional_clicks_fail(*args)

    def _verify_move_to_fails(self, *args):
        from ImageHorizonLibrary import MouseException
        with self.assertRaises(MouseException):
            self.lib.move_to(*args)

    def test_move_to(self):
        for args in [(1, 2), ((1, 2),), ('1', u'2'), ((u'1', '2'),)]:
            self.lib.move_to(*args)
            self.assertEquals(self.mock.moveTo.mock_calls, [call(1, 2)])
            self.mock.reset_mock()

        for args in [(1,),
                     (1, 2, 3),
                     (u'1', u'lollerskates'),
                     ((u'1', u'lollerskates'),)]:
            self._verify_move_to_fails(*args)

    def test_mouse_down(self):
        for args in [tuple(), ('right',)]:
            self.lib.mouse_down(*args)
        self.assertEquals(self.mock.mouseDown.mock_calls, [call('left'), call('right')])

    def test_mouse_up(self):
        for args in [tuple(), ('right',)]:
            self.lib.mouse_up(*args)
        self.assertEquals(self.mock.mouseUp.mock_calls, [call('left'), call('right')])
