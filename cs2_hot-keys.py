#!/usr/bin/env python3
import inspect
import logging
from time import sleep

# Try importing two modules that have to be installed with pip first
try:
	import pyautogui
except ImportError:
	raise SystemExit("Missing required module 'pyautogui', install it with pip:\npip3 install pyautogui")
try:
	import keyboard
except ImportError:
	raise SystemExit("Missing required module 'keyboard', install it with pip:\npip3 install keyboard")

# SETTINGS

# Hotkeys
ACTIVATION_HOTKEY:str = "F9" # <-- Button to activate this script
DEACTIVATION_HOTKEY:str = "F8" # <-- Button to deactivate this script
GAME_DISCONNECT_HOTKEY:str = "F1"  # <-- other ideas: 'd' (for 'disconnect'), F1
GAME_QUIT_HOTKEY:str = "F2"        # <-- other ideas: 'q' (for 'quit'), F2
STOP_SCRIPT_HOTKEY:str = "F4" # <-- other ideas: 'left_ctrl'

# Delays
TOGGLE_CONSOLE_DELAY:float = 0.002
WRITE_CONSOLE_DELAY:float = 0.002
ACTION_WAIT_DELAY:float = 0.002
SWITCH_STATE_DELAY:float = 1.8

# Script
activated:bool = False

# ANSI Colors
CL_RESET:str = "\033[0m"  	# Reset to default color
RED:str = "\033[31m"		# Warning/Critical things
YELLOW:str = "\033[33m"		# Action names/titles
CYAN:str = "\033[36m"		# For Hot keys
BLUE:str = "\033[34m"		# Not used for now
GREEN:str = "\033[32m"		# For activated state
GRAY:str = "\033[90m"		# For deactivated state

# Logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'  #date format: Day, Month, Year. Hour, Minute, Second
)
logging.getLogger().setLevel(logging.INFO)

def hotkeys_info() -> str:
#	The first arrow (->) just couldn't get well alligned with the others
#	So have to use '.ljust'. It left-justifies 'text' with a total width of 20 chars
	return f"""Action Hotkeys (while activated):

GAME_DISCONNECT   -> {CYAN}{GAME_DISCONNECT_HOTKEY.ljust(20)}{CL_RESET}
GAME_QUIT         -> {CYAN}{GAME_QUIT_HOTKEY}{CL_RESET}
STOP_SCRIPT       -> {CYAN}{STOP_SCRIPT_HOTKEY}{CL_RESET}
{f'DEACTIVATE_SCRIPT -> {CYAN}{DEACTIVATION_HOTKEY}{CL_RESET}' if ACTIVATION_HOTKEY != DEACTIVATION_HOTKEY else ''}
"""

def toogle_console() -> None:
	pyautogui.press('`')
	sleep(TOGGLE_CONSOLE_DELAY)

def game_quit() -> None:
#	This 'inspect' lets me get the function name inside of which this piece of code is beeing executed
#	Scince its called 'game_quit', it's going to be written in the CLI this func. name
#	Because the function name tells by itself what its designed for
	current_func_name:str = inspect.currentframe().f_code.co_name
	logging.info(f"Toogled action '{YELLOW}{current_func_name}{CL_RESET}'")

	toogle_console()
	pyautogui.write('quit'); sleep(WRITE_CONSOLE_DELAY)
	pyautogui.press('enter')
	toogle_console()

def game_disconnect() -> None:
	current_func_name:str = inspect.currentframe().f_code.co_name
	logging.info(f"Toogled action '{YELLOW}{current_func_name}{CL_RESET}'")

	toogle_console()
	pyautogui.write('disconnect'); sleep(WRITE_CONSOLE_DELAY)
	pyautogui.press('enter')
	toogle_console()

def switch_active_state() -> None:
	global activated
	if activated is True:
		logging.info(f"CS2 Hotkeys {GRAY}Deactivated{CL_RESET}")
		activated = False
	else:
		logging.info(f"CS2 Hotkeys {GREEN}Activated{CL_RESET}")
		activated = True


def do_action() -> None:
	global activated # <-- need to access the Boolean

	if keyboard.is_pressed(GAME_DISCONNECT_HOTKEY):
		game_disconnect()

	elif keyboard.is_pressed(GAME_QUIT_HOTKEY):
		game_quit()

	elif keyboard.is_pressed(DEACTIVATION_HOTKEY):
		switch_active_state()

	elif keyboard.is_pressed(STOP_SCRIPT_HOTKEY):
		print("Пока-пока, Бай-бай. 👋")
		raise SystemExit(0)


def main() -> None:
#	Print 'and deactivate' text if the variable ACTIVATION_HOTKEY has the same value as DEACTIVATION_HOTKEY
	print(f"Press {CYAN}{ACTIVATION_HOTKEY}{CL_RESET} to activate{' and deactivate' if ACTIVATION_HOTKEY == DEACTIVATION_HOTKEY else ''} the script...\n")
	print ( hotkeys_info() )

	"""Unfortunately (as of now), a delay is needed after detecting act. hotkey (if it's same as deact.  hotkey)
	Because without delay, after switching states (not active --> active),
	The next if statement is already checking for the same ACTIVATION_HOTKEY beeing pressed
	And scinces the code is happening so fast, by the time user activated the script by hotkey,
	The script already starts to check if it's beeing pressed to deactivate it."""

	while True:
	    keyboard.wait(ACTIVATION_HOTKEY)
	    switch_active_state()

	    if ACTIVATION_HOTKEY == DEACTIVATION_HOTKEY:
	    	sleep (SWITCH_STATE_DELAY)
			
	    while activated:
	        do_action()
	        sleep(ACTION_WAIT_DELAY)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		logging.info(f"{YELLOW}CTRL+C{CL_RESET} Detected. Пока-пока, Бай-бай. 👋")
		raise SystemExit(0)
