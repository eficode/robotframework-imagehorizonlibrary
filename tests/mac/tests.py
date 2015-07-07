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

    def test_open_application(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.open_application('/Applications/Calculator.app')
        lib.wait_for('calculator active')
        lib.press_combination('key.command', 'q')
        lib.open_application('Calculator')
        lib.wait_for('calculator active')
        lib.press_combination('key.command', 'q')
        lib.open_application('Calculator.app')
        lib.wait_for('calculator active')
        lib.press_combination('key.command', 'q')


    def test_calculator(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.open_application('Calculator')
        lib.type('notepad', 'Key.enter')
        lib.wait_for('notepad active')
        lib.type('I love ImageHorizonLibrary', 'key.enter')
        lib.type_with_keys_down('shift makes me shout', 'key.shift',
                                pause='0.1', interval=0.05)
        lib.press_combination('KEY.CTRL', 'a')
        lib.press_combination('KeY.cTrL', 'c')
        lib.type('key.Enter')
        lib.press_combination('Key.ctrl', 'V')

def suite():
    tests = [
                'test_empty_lib_initialization',
                'test_open_application',
                #'test_notepad_with_images',
            ]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))

def main():
    unittest.TextTestRunner().run(suite())
