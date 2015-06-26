import unittest
import os, time
import pykuli

REFERENCE_IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reference_images')
os.environ['REFERENCE_IMAGE_FOLDER'] = REFERENCE_IMAGE_FOLDER

class TestWindowsWithImages(unittest.TestCase):
	
	def test_notepad_with_images(self):
		pykuli.click_image('Start.png')
		pykuli.typewrite('notepad')
		pykuli.press('enter')
		pykuli.locate_image('Notepad_icon.png')
		pykuli.locate_image('Notepad_untitled.png')
		pykuli.typewrite('echo "I love pykuli"')
		pykuli.hotkey('ctrl', 'a')
		pykuli.hotkey('ctrl', 'c')
		pykuli.click_image('Start.png')
		pykuli.typewrite('command')
		pykuli.press('enter')
		pykuli.click_image('Command_prompt_administrator.png', 'right')
		pykuli.moveTo(pykuli.locate_image('Command_prompt_edit.png'))
		pykuli.click_image('Command_prompt_paste.png')
		pykuli.press('enter')
		time.sleep(3)
		pykuli.click_image('Command_prompt_administrator.png', 'right')		
		pykuli.press('c')
		pykuli.click_image('Notepad_unselected.png')
		pykuli.hotkey('alt', 'f4')
		pykuli.press('right')
		pykuli.press('enter')

def suite():
    tests = [
    			'test_notepad_with_images',
    		]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))
	
def main():
	unittest.TextTestRunner().run(suite())
