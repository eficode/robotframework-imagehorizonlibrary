import time
import unittest
from os.path import dirname, join as path_join, realpath


from ImageHorizonLibrary import ImageHorizonLibrary

REFERENCE_IMAGE_FOLDER = path_join(dirname(realpath(__file__)), 'reference_images')

class TestWindowsWithImages(unittest.TestCase):

    def test_empty_lib_initialization(self):
        lib = ImageHorizonLibrary()
        self.assertTrue(lib)

    def test_open_application(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.launch_application('Calc.exe')
        lib.wait_for('calculator active', '8')
        lib.press_combination('key.alt', 'key.f4')

    def test_notepad_with_images(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)
        lib.type('Key.WIN', 'notepad', 'Key.enter')
        lib.wait_for('notepad active')
        lib.type('I love ImageHorizonLibrary', 'key.enter')
        lib.type_with_keys_down('shift makes me shout', 'key.shift', pause='0.1', interval=0.05)
        lib.press_combination('KEY.CTRL', 'a')
        lib.press_combination('KeY.cTrL', 'c')
        lib.type('key.Enter')
        lib.press_combination('Key.ctrl', 'V')
        lib.press_combination('key.alt', 'key.F4')
        lib.type('key.right', 'key.enter')

def suite():
    tests = [
                'test_empty_lib_initialization',
                'test_open_application',
                'test_notepad_with_images',
            ]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))

def main():
    unittest.TextTestRunner().run(suite())
