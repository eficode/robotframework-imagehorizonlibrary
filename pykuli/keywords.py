import os
import pyautogui as ag

ag.FAILSAFE = True

def hotkey(*args, **kwargs):
	ag.hotkey(*args, **kwargs)

def moveTo(*args, **kwargs):
	ag.moveTo(*args, **kwargs)

def press(*args, **kwargs):
	ag.press(*args, **kwargs)

def typewrite(*args, **kwargs):
	ag.typewrite(*args, **kwargs)

def click_image(ref_image, button='left'):
	image_center_location = ag.center(locate_image(ref_image))
	ag.click(image_center_location, button=button)
	return image_center_location

def locate_image(ref_image):
	REFERENCE_IMAGE_FOLDER = os.environ.get('REFERENCE_IMAGE_FOLDER')
	if REFERENCE_IMAGE_FOLDER is None:
		raise Exception('set environment variable REFERENCE_IMAGE_FOLDER to the path of the directory containing the reference images.')
	location = ag.locateOnScreen(REFERENCE_IMAGE_FOLDER+os.sep+ref_image)
	if location is None:
		raise Exception('Failed to locate image '+REFERENCE_IMAGE_FOLDER+os.sep+ref_image+' on the screen. Sorry.')
	return location


