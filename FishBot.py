import win32gui
import time, sys
import pyautogui
import Splash_Detection
from win32api import GetSystemMetrics
from random import *
from Keyboard import *


# Global variables
# -----------------
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
SEARCH_BOX = 4*[0]  # [x0, x1, y0, y1]
FISH_KEY = []
TIME_FISHING = 0  # Time (s)
REACTION_TIME = 0.3  # Reaction time to loot hook


# Initialize parameters.
def init():
    global SEARCH_BOX, TIME_FISHING, WINDOW_WIDTH, WINDOW_HEIGHT

    WINDOW_WIDTH = GetSystemMetrics(0)
    WINDOW_HEIGHT = GetSystemMetrics(1)
    SEARCH_BOX[0] = int(round(WINDOW_WIDTH/8))       # x0
    SEARCH_BOX[1] = int(round(7*WINDOW_WIDTH/8))     # x1
    SEARCH_BOX[2] = int(round(WINDOW_HEIGHT/4.5))    # y0
    SEARCH_BOX[3] = int(round(3*WINDOW_HEIGHT/4.5))  # y1
    print('Search box: ', SEARCH_BOX[:])
    check_fishing_key()
    check_game()
    mouse_pos((SEARCH_BOX[0], SEARCH_BOX[2]))  # To prevent cursor on bobber initially


# Run Fishing Bot
def run():
    start_time = time.time()
    while time.time()-start_time <= TIME_FISHING:
        check_game()  # In case game not in focus
        login()
        start_session = time.time()
        while time.time()-start_session <= fish_session():  # Default 15-20 min
            fish(FISH_KEY)
            if find_hook() is True:
                if Splash_Detection.hook_listener() is True:
                    time.sleep(REACTION_TIME)
                    loot_hook()
                else:
                    print("No fish caught.")
        logout()
        if time.time() - start_time <= TIME_FISHING:
            anti_afk()


# Set World of Warcraft in focus.
def check_game():
    try:
        window_handle = win32gui.FindWindow(None, "World of Warcraft")
        win32gui.SetForegroundWindow(window_handle)
        time.sleep(.1)
    except win32gui.error:
        print("World of Warcraft not found!\n")
        print("System exit.")
        sys.exit(0)


# Set the fishing key
def check_fishing_key():
    global FISH_KEY  # Use Global keyword to change a global variable
    FISH_KEY = pyautogui.prompt('What key is fishing on? (small letters)', 'Fish button')
    if not FISH_KEY:
        pyautogui.alert('Please select a key!', 'Warning!')
        print("System exit.")
        sys.exit(0)  # Exit(0) for safe exit
    time.sleep(.1)


# Search for hook in the area defined by SEARCH_BOX
def find_hook():
    print("Searching hook...")
    old_mouse = win32gui.GetCursorInfo()[1]  # Return int of mouse icon. Will change if mouse icon change.
    for y in range(SEARCH_BOX[2], SEARCH_BOX[3], 50):
        for x in range(SEARCH_BOX[0], SEARCH_BOX[1], 60):
            mouse_pos((x, y))
            time.sleep(.05)
            current_mouse = win32gui.GetCursorInfo()[1]
            if current_mouse != old_mouse:
                print("Hook found!")
                time.sleep(.1)
                return True
    return False


# Login function, sleep between 15 and 25 seconds
def login():
    print("Logging in.")
    login_x = int(round(WINDOW_WIDTH/2.02))
    login_y = int(round(WINDOW_HEIGHT/1.17))
    mouse_pos((login_x, login_y))
    left_click()
    time.sleep(1)
    mouse_pos((SEARCH_BOX[0], SEARCH_BOX[2]))
    time.sleep(uniform(15, 25))


# Logout function, sleep for 25 seconds
def logout():
    print("Logging out.")
    menu_x = int(round(WINDOW_WIDTH/1.56))
    menu_y = int(round(WINDOW_HEIGHT/1.07))
    logout_x = int(round(WINDOW_WIDTH/2))
    logout_y = int(round(WINDOW_HEIGHT/1.93))
    mouse_pos((menu_x, menu_y))
    left_click()
    time.sleep(1)
    mouse_pos((logout_x, logout_y))
    left_click()
    time.sleep(25)


# How long a fishing session should last. Default value between 15 and 20 minutes.
def fish_session(t_0=900, t_final=1200):
    return uniform(t_0, t_final)


# Anti AFK function at login screen. Default value is uniformly picked between 10 and 15 minutes.
def anti_afk(t_0=600, t_final=900):
    mouse_pos((SEARCH_BOX[0], SEARCH_BOX[2]))
    afk_time = time.time()+uniform(t_0, t_final)
    while time.time() <= afk_time:
        hold_key('down_arrow')
        release_key('down_arrow')
        time.sleep(5)
        hold_key('up_arrow')
        release_key('up_arrow')
        time.sleep(5)


# Loot bobber
def loot_hook():
    print("Looting hook.")
    hold_key('shift')
    right_click()
    release_key('shift')
    time.sleep(3)
    mouse_pos((SEARCH_BOX[0], SEARCH_BOX[2]))


# Cast bobber, sleep between 0 to 3 seconds for realistic appearance.
def fish(button):
    time.sleep(uniform(0, 3))
    hold_key(button)
    release_key(button)
    print("Casting bobber.")
    time.sleep(1)


def main():
    init()
    try:
        run()
    except KeyboardInterrupt:
        print("Program closed.")
    pyautogui.alert('Fish bot complete.', 'Thanks for using Fish bot')

if __name__ == '__main__':
    main()
