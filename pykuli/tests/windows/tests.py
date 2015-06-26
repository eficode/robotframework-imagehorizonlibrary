import unittest, os
import pyautogui as ag

from pykuli.tests.windows.constants import REFERENCE_IMAGES_FOLDER

ag.FAILSAFE = True
SCREEN_WIDTH = ag.size()[0]
SCREEN_HEIGHT = ag.size()[1]

def click_image(ref_image, button='left'):
	location = ag.locateOnScreen(REFERENCE_IMAGES_FOLDER+os.sep+ref_image)
	ag.click(ag.center(location), button=button)

def locate_image(ref_image):
	return ag.locateOnScreen(REFERENCE_IMAGES_FOLDER+os.sep+ref_image)

class TestWindowsWithImages(unittest.TestCase):
	
	def test_command_prompt(self):
		ag.moveTo(26, 777)
		ag.click()
		ag.typewrite('cmd')
		ag.press('enter')
		ag.typewrite('dir')
		ag.press('enter')

	def test_notepad_with_images(self):
		click_image('Start.png')
		ag.typewrite('notepad')
		ag.press('enter')
		locate_image('Notepad_icon.png')
		locate_image('Notepad_untitled.png')
		ag.typewrite('echo "Sakke on homo"')
		ag.hotkey('ctrl', 'a')
		ag.hotkey('ctrl', 'c')
		click_image('Start.png')
		ag.typewrite('command')
		ag.press('enter')
		click_image('Command_prompt_administrator.png', 'right')
		ag.moveTo(ag.center(locate_image('Command_prompt_edit.png')))
		click_image('Command_prompt_paste.png')
		ag.press('enter')

def suite():
    tests = [
    			'test_command_prompt', 
    			'test_notepad_with_images',
    		]
    return unittest.TestSuite(map(TestWindowsWithImages, tests))
	
def main():
	unittest.TextTestRunner().run(suite())
