import win32gui, win32con
import mss
import time
from PIL import Image
import cv2
import numpy as np
import pyautogui
from enum import Enum
import imageCompareHandler
import keyboard


window = None

class Window:
    def __init__(self,x,y,w,h,wnd_object) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.wnd_object = wnd_object
    
    def get_for_mss(self):
        return {"top":self.y, "left":self.x,"width":self.w,"height":self.h}
    
    
    
def callback(hwnd, extra):
    global window
    if window is None:
        window_title = win32gui.GetWindowText(hwnd)
        if window_title.__contains__("mGBA -"):
            window_found = True
            #this is the correct window
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            print("Window %s:" % window_title)
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (w, h))
            win32gui.SetForegroundWindow(hwnd)
            window  = Window(x,y,w,h,hwnd)
            return False
    else:
        return False #False should stop the enumeration
    
def get_window():
    try:
        win32gui.EnumWindows(callback, None)
    except Exception as e:
        if not str(e).__contains__("No error message is available"):
            raise e
        
class ScreenCapturer():
    def __init__(self):
        self.capturing = False
        
   
    def start_capturing(self,callback,capture_rate=100):
        get_window()
        global window
        while window is None:
            time.sleep(1)
            global window
            
        capture_sleep_time = 1/capture_rate
        
        previous_time = time.time()
        
        with mss.mss() as sct:
            sct_img = sct.grab(window.get_for_mss())
            raw = np.array(sct_img)
            scaleHandler = imageCompareHandler.ImageScaleHandler(raw)
            self.capturing = True
            while self.capturing:
                if keyboard.is_pressed('esc'):
                    print("User exited with ESC")
                    return
                if(time.time() - previous_time) >= capture_sleep_time:
                    previous_time = time.time()
                    raw = np.array(sct.grab(window.get_for_mss()))  
                    callback(raw)
        
    def stop_capturing(self):
        self.capturing = False