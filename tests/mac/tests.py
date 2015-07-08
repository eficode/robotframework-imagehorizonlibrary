import time
import unittest
from os.path import dirname, join as path_join, realpath


from ImageHorizonLibrary import ImageHorizonLibrary

REFERENCE_IMAGE_FOLDER = path_join(dirname(realpath(__file__)),
                                           'reference_images')

class TestWindowsWithImages(unittest.TestCase):

    def test_empty_lib_initialization(self):
        lib = ImageHorizonLibrary()
        self.assertTrue(lib)

    def test_open_and_close_application(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        alias1 = lib.launch_application('open -a /Applications/Calculator.app')
        lib.wait_for('calculator active')
        lib.terminate_application(alias1)
        lib.launch_application('open -a Calculator', alias='My calculator')
        lib.wait_for('calculator active')
        lib.terminate_application('My calculator')
        lib.launch_application('open -a Calculator.app')
        lib.wait_for('calculator active')
        lib.terminate_application()

    def test_calculator(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.launch_application('open -a Calculator')
        lib.wait_for('calculator active')
        button_5_pos = lib.click_image('button 5')
        lib.click_image('button plus')
        lib.move_to(button_5_pos)
        lib.click()
        lib.click_image('button equals')
        lib.wait_for('result 10')
        lib.press_combination('key.command', 'q')

    def test_click_to_directions(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.launch_application('open -a Calculator')
        lib.wait_for('calculator active')
        button_5_pos = lib.locate('button 5')
        lib.click_to_the_left_of(button_5_pos, '56', clicks='2',
                             button='left', interval='0.0')
        lib.click_to_the_above_of(button_5_pos, '56', clicks='2',
                             button='left', interval='0.0')
        lib.click_to_the_right_of(button_5_pos, '56', clicks='2',
                             button='left', interval='0.0')
        lib.click_to_the_below_of(button_5_pos, '56', clicks='2',
                             button='left', interval='0.0')
        lib.wait_for('result 44886622')
        lib.terminate_application()


def suite():
    tests = [
                'test_empty_lib_initialization',
                'test_open_and_close_application',
                'test_calculator',
                'test_click_to_directions',
            ]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))

def main():
    unittest.TextTestRunner().run(suite())
