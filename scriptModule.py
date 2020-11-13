
#py -m pip install pynput
import pyautogui
import keyboard
import threading
import time
import os

from pynput.keyboard import Listener as KeyListener
from pynput.keyboard import Controller as KeyController
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button as MouseButton
import logging
from datetime import datetime

# Gets a button as string and returns the button object
# @buttonString: Button as string
def stringToButton(buttonString):
	switcher={
		'Button.left':MouseButton.left,
		'Button.right':MouseButton.right,
		'Button.middle':MouseButton.middle
	}
	# If no button can be found return left button
	return switcher.get(buttonString,MouseButton.left)

# Gets a key as string and returns the key object
# @keyString: Key as string
def stringToKey(keyString):
	switcher={
		'Key.shift':Key.shift,
		'Key.enter':Key.enter,
		'Key.alt':Key.alt,
		'Key.alt_l':Key.alt_l,
		'Key.alt_r':Key.alt_r,
		'Key.alt_gr':Key.alt_gr,
		'Key.backspace':Key.backspace,
		'Key.caps_lock':Key.caps_lock,
		'Key.cmd':Key.cmd,
		'Key.cmd_l':Key.cmd_l,
		'Key.cmd_r':Key.cmd_r,
		'Key.ctrl':Key.ctrl,
		'Key.ctrl_l':Key.ctrl_l,
		'Key.ctrl_r':Key.ctrl_r,
		'Key.delete':Key.delete,
		'Key.down':Key.down,
		'Key.end':Key.end,
		'Key.esc':Key.esc,
		'Key.f1':Key.f1,
		'Key.f2':Key.f2,
		'Key.f3':Key.f3,
		'Key.f4':Key.f4,
		'Key.f5':Key.f5,
		'Key.f6':Key.f6,
		'Key.f7':Key.f7,
		'Key.f8':Key.f8,
		'Key.f9':Key.f9,
		'Key.f10':Key.f10,
		'Key.f11':Key.f11,
		'Key.f12':Key.f12,
		'Key.f13':Key.f13,
		'Key.f14':Key.f14,
		'Key.f15':Key.f15,
		'Key.f16':Key.f16,
		'Key.f17':Key.f17,
		'Key.f18':Key.f18,
		'Key.f19':Key.f19,
		'Key.f20':Key.f20,
		'Key.home':Key.home,
		'Key.left':Key.left,
		'Key.page_down':Key.page_down,
		'Key.page_up':Key.page_up,
		'Key.right':Key.right,
		'Key.shift':Key.shift,
		'Key.shift_l':Key.shift_l,
		'Key.shift_r':Key.shift_r,
		'Key.space':Key.space,
		'Key.tab':Key.tab,
		'Key.up':Key.up,
		'Key.media_play_pause':Key.media_play_pause,
		'Key.media_volume_mute':Key.media_volume_mute,
		'Key.media_volume_down':Key.media_volume_down,
		'Key.media_volume_up':Key.media_volume_up,
		'Key.media_previous':Key.media_previous,
		'Key.media_next':Key.media_next,
		'Key.insert':Key.insert,
		'Key.menu':Key.menu,
		'Key.num_lock':Key.num_lock,
		'Key.pause':Key.pause,
		'Key.print_screen':Key.print_screen,
		'Key.scroll_lock':Key.scroll_lock
	}
	# If no key can be found return enter key
	return switcher.get(keyString,Key.enter)

			
# Plays a defined macro
# @time: Array with waiting time before the event
# @type: Array with types of the event (Mouse or Key)
# @action: Array with actions of the event
# @details: Array with details for the event
def playScript(waitingTime, type, action, details):
	eventCount = 0
	mouse = MouseController()
	keyboard = KeyController()
	for t in waitingTime:
		time.sleep(int(t) / 1000)
		if type[eventCount]  == 'Mouse':
			if action[eventCount]  == 'Scrolled':
				# Move mouse to the right position
				arguments = details[eventCount].split(" ", 1)
				coordinates = arguments[0].split(",", 1)		
				xpos = coordinates[0][1:]
				ypos = coordinates[1][:-1]
				mouse.position = (coordinates[0][1:], coordinates[1][:-1])
				
				# Get the right scroll arguments and perform scroll
				scrollArgs = arguments[1].split(",", 1)
				stArg = scrollArgs[0][1:]
				ndArg = scrollArgs[1][:-1]
				mouse.scroll(int(stArg), int(ndArg))
			else:
				# Move mouse to the right position
				coordinates = details[eventCount].split(",", 1)
				xpos = coordinates[0][1:]
				ypos = coordinates[1][:-1]
				mouse.position = (xpos, ypos)
				# Press and release
				mouse.press(stringToButton(str(action)))
				mouse.release(stringToButton(str(action)))
		else:
			# Remove quotation marks
			event = action[eventCount].replace("'","")
			if details[eventCount]  == 'Press':
				if len(event) == 1:
					keyboard.press(event)
				else:
					keyboard.press(stringToKey(event))
			else:
				if len(event) == 1:
					keyboard.release(event)
				else:
					keyboard.release(stringToKey(event))

		eventCount += 1
	
# Parses a script file from the recorder and returns the macro script
# @scriptFile: Input script file which will be parsed
def parseScript(scriptFile):
	# Using readlines() 
	script = open(scriptFile, 'r') 
	scriptLines = script.readlines() 
	
	# Timestamp of the last action
	lastTimeStamp = 0
	lastDate = 0
	
	# Arrays for the output
	waitingTime = []
	type = []
	action = []
	details = []
  
	# Parse each line of the script file
	for line in scriptLines:
		# Remove quotation marks
		line.replace("'","")
		# Split line in segments
		segments = line.split()
		# print(segments)
		# Calculate waiting time 
		newTimeStamp = segments[0] + "T" + segments[1]
		# Remove last char ":"
		newTimeStamp = newTimeStamp[:-1]
		format = "%Y-%m-%dT%H:%M:%S,%f"
		datetime_obj = datetime.strptime(newTimeStamp, format)
		if lastTimeStamp == 0:
			waitingTime.append(0)
		else:
			# Get milliseconds between this action and the last one
			timepassed = datetime_obj.timestamp() - lastTimeStamp.timestamp()
			deltaMS = timepassed * 1000
			# Cut everything after the milliseconds
			split_ms = str(deltaMS).split(".", 1)
			waitingTime.append(split_ms[0])
		
		# Save for next action
		lastTimeStamp = datetime_obj
		# Get the type of the action
		if segments[2] == 'Mouse':
			type.append("Mouse") 
			action.append(segments[3])
			# Check if it is a click or scrolled
			if segments[3] == 'Scrolled': 
				details.append(segments[5] + " " + segments[6])
			else:
				details.append(segments[4])			
		else:
			type.append("Key")
			action.append(segments[2])
			details.append(segments[3])
	
	return waitingTime, type, action, details

# Listener definition for mouse click		
def on_click(x, y, button, pressed):
	if pressed:
		logging.info('Mouse {2} ({0},{1})'.format(x, y, button))

# Listener definition for mouse scroll		
def on_scroll(x, y, dx, dy):
	logging.info('Mouse Scrolled at ({0},{1}) ({2},{3})'.format(x, y, dx, dy))

# Listener definition for key press		
def on_press(key):
	logging.info(str(key) + " Press")

# Listener definition for key released	
def on_release(key):
	logging.info(str(key) + " Release")
	if key == Key.ctrl_r:
		# Stop listener
		return False

# Mouse listener	
def startMouseRecorder():
	with MouseListener(on_click=on_click, on_scroll=on_scroll) as listener:
		listener.join()

# Function to record all keyboard and mouse input into a local file until the right control button is hit	
def startRecorder():
	print("Key and mouse listener started: %s" % time.ctime())
	print("!!!Press Right Control Button to stop recording!!!")
	# Define the location of the logs
	logging.basicConfig(filename = ("keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
	
	#Start a new Thread for the mouse listener
	thMouseListener = threading.Thread(target=startMouseRecorder)
	thMouseListener.daemon = True
	thMouseListener.start()
	
	#Start the key listener and wait for it to end
	with KeyListener(on_press=on_press, on_release=on_release) as listener:
		listener.join()
	
	print("Key and mouse listener stopped: %s" % time.ctime())
		
# Deletes the local key log file			
def clearRecordFile():
	if os.path.exists("keyLog.txt"):
		os.remove("keyLog.txt")
	else:
		print("No Record file found: %s" % time.ctime())
