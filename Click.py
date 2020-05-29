# To Install:
#          ? 1. Download and Install Python3.8 64Bit https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe
#               !   1a. Be sure to click "add Python to PATH" during install
#          ? 2. Once installed, Open Powershell in Administrator
#          ? 3. In PowerShell enter "pip install pynput"

import time
import os
import shutil
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

import random
import json


def programStart():
    os.system('cls')
    menu = "Main"
    print(prettyPrinter("menu_page", menu))
    print(prettyPrinter("current_settings", 'n/a'))
    print(bcolors.FAIL + "For issues and support, go to https://github.com/GetParanoid/AutoClicker/issues" + bcolors.ENDC)
    userInput = input("\n[ 1 ] - Clicker \n[ 2 ] - Settings\n\nINPUT: ")
    os.system('cls')
    if userInput == "1":
        print(prettyPrinter('controls', 'n/a'))
    elif userInput == "2":
        settingsMenu()
        os.system('pause')
    else:
        print("Invalid input")
        time.sleep(2)
        os.system('cls')
        programStart()

def settingsMenu():
    os.system('cls')

    menu = "Settings"
    print(prettyPrinter("menu_page", menu))
    print(prettyPrinter("current_settings", 'n/a'))

    userInput = input("\n[ 1 ] - Click Intervals \n[ 2 ] - Hotkeys \n[ 3 ] - MAIN MENU \n\nINPUT: ")
    if userInput == "1":
        os.system('cls')
        ClickIntervals()
    elif userInput == "2":
        print("Coming Soon")
        programStart()
    elif userInput == "3":
        programStart()

def ClickIntervals():
    os.system('cls')
    menu = "Click Intervals"
    print(prettyPrinter("menu_page", menu))
    print(prettyPrinter("current_settings", 'n/a'))
    selectedSetting = input('\n[ 1 ] - Change Min Delay\n[ 2 ] - Change Max delay\n[ 3 ] - Back\n\nINPUT: ')
    if selectedSetting == "1":
        os.system('cls')
        minDelay = input("\nMinimum Delay\n\nINPUT: ")
        setting = "click.minDelay"
        newValue = minDelay
        if getSetting("click.maxDelay") < newValue:
            os.system('cls')
            print(prettyPrinter("current_settings", 'n/a'))
            print(bcolors.FAIL + "Min Delay Cannot Be Higher Than Max Delay" + bcolors.ENDC)
            time.sleep(3)
            ClickIntervals()
    elif selectedSetting == "2":
        os.system('cls')
        print(prettyPrinter("current_settings", 'n/a'))
        maxDelay = input("\nMax Delay\n\nINPUT: ")
        setting = "click.maxDelay"
        newValue = maxDelay
        if getSetting("click.minDelay") > newValue:
            os.system('cls')
            print(bcolors.FAIL + "Max Delay Cannot Be Lower Than Min Delay" + bcolors.ENDC)
            time.sleep(3)
            ClickIntervals()
    elif selectedSetting == "3":
        settingsMenu()
    os.system('cls')
    changeSetting(setting, newValue)

def prettyPrinter(group, menu):
    if group == "current_settings":
        return(
            bcolors.BOLD + "\nCurrent Settings\n" + bcolors.ENDC +
            bcolors.HEADER + "----------------------------------------------------------------\n" + bcolors.ENDC +
            "Min Click Delay: " + bcolors.OKGREEN + getSetting("click.minDelay")  + bcolors.ENDC + '\nMax Click Delay: ' + bcolors.FAIL + getSetting("click.maxDelay") + bcolors.ENDC +
            bcolors.HEADER + "\n----------------------------------------------------------------\n" + bcolors.ENDC
            )
    elif group == "menu_page":
        menu = menu.center(15)
        return (
            bcolors.UNDERLINE + 'MENU: ' + menu + bcolors.ENDC
        )
    elif group == 'controls':
        return (
           bcolors.FAIL + "Key: O To Toggle Clicking On/Off" + "\nKey: P To Emergency Close Program"  + bcolors.ENDC
        )

def changeSetting(setting, newValue):
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + '/gxpSettings.json') as f:
        data = json.load(f)

    for settings in data['settings']:

        if settings['name'] == setting:
            settings['value'] = newValue
            print("Updated " + setting + " to " + newValue)

    with open('gxpSettings.json', 'w') as f:
        json.dump(data, f, indent=2)

    ClickIntervals()

def getSetting(setting):
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + '/gxpSettings.json') as f:
        data = json.load(f)

    for settings in data['settings']:
        if settings['name'] == setting:
            return  settings['value']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

delay = 10
button = Button.left
start_stop_key = KeyCode(char='o') # ! O Key to Start
exit_key = KeyCode(char='p')       # ! P Key to Stop

programStart()

###################### ! Start Clicking Logic 
def startClicker():
    # delay = 10
    # button = Button.left
    # start_stop_key = KeyCode(char='o') # ! O Key to Start
    # exit_key = KeyCode(char='p')       # ! P Key to Stop
    os.system('pause')



# Testing https://www.yorku.ca/nmw/datt1939f18/javascript_all/js_timebetweenclicks.html#
class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False
        programStart()

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:

                os.system('cls')
                menu = "Clicking"
                print(prettyPrinter("menu_page", menu))
                print(prettyPrinter("current_settings", 'n/a'))
                print(prettyPrinter('controls', 'n/a'))

                mouse.click(self.button)
                actualDelay = random.uniform(float(getSetting("click.minDelay")), float(getSetting("click.maxDelay"))) # ? This is the value of time between clicks
                print("\n\nLast Click - [" + str(round(actualDelay, 3)) + "] Seconds")
                time.sleep(actualDelay)
            time.sleep(0.1)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
            print("Stopped Clicking")
        else:
            click_thread.start_clicking()
            print("Started Clicking")
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
