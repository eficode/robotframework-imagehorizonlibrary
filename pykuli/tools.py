import pyautogui, sys
import argparse, time

def demonstrate():
    return "Pykuli seems to be working. You just called demonstrate from pykuli.tools"

def monitor_mouse():
	while True:
		time.sleep(1)
		print pyautogui.position()

def main():
    parser = argparse.ArgumentParser(description='Tools for creating and deploying nodes')
    parser.add_argument("-mm", "--monitor_mouse", help="print mouse movement", action="store_true")    

    args = parser.parse_args()
    arg_count = len([1 for v in vars(args).values() if v])

    if args.monitor_mouse:
    	monitor_mouse()

if __name__ == '__main__':
	main()