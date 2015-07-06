import time
import unittest
from os.path import dirname, join as path_join, realpath


from ImageHorizonLibrary import ImageHorizonLibrary

REFERENCE_IMAGE_FOLDER = path_join(dirname(realpath(__file__)), 'reference_images')

class TestWindowsWithImages(unittest.TestCase):

    def test_empty_lib_initialization(self):
        lib = ImageHorizonLibrary()
        self.assertTrue(lib)

    def test_notepad_with_images(self):
        lib = ImageHorizonLibrary(REFERENCE_IMAGE_FOLDER)

        lib.press('Key.WIN')
        lib.type('notepad', 'Key.enter')
        lib.wait('icon Notepad')



        #lib.click_image('Start.png')
        #lib.typewrite('notepad')
        #lib.press('enter')
        #lib.locate_image('Notepad_icon.png')
        #lib.locate_image('Notepad_untitled.png')
        #lib.typewrite('echo "I love lib"')
        #lib.hotkey('ctrl', 'a')
        #lib.hotkey('ctrl', 'c')
        #lib.click_image('Start.png')
        #lib.typewrite('command')
        #lib.press('enter')
        #lib.click_image('Command_prompt_administrator.png', 'right')
        #lib.moveTo(lib.locate_image('Command_prompt_edit.png'))
        #lib.click_image('Command_prompt_paste.png')
        #lib.press('enter')
        #time.sleep(3)
        #lib.click_image('Command_prompt_administrator.png', 'right')
        #lib.press('c')
        #lib.click_image('Notepad_unselected.png')
        #lib.hotkey('alt', 'f4')
        #lib.press('right')
        #lib.press('enter')

def suite():
    tests = [
                'test_notepad_with_images',
            ]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))

def main():
    unittest.TextTestRunner().run(suite())
