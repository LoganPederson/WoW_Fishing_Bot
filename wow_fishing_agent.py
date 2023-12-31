import cv2 as cv
import numpy as np
import os
import pyautogui
from time import *
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from tkinter import *
import sys
import msvcrt
import random


class FishingAgent:  

    def __init__(self):
        self.exitPlease = False
        self.wincap = WindowCapture()
        self.bobber_eye = Vision('bobber_eye.jpg')
        self.feather_pretty_far = Vision('feathers_both_1080_prettyfar.jpg') #0.78 and >4s works medium at far and at night 
        self.starting_position = False
        self.weight = 0.7
        self.starting_time = 0
        self.tracking = None
        #0.65 working well up close, not so great at distance using bobber_eye_eye.jpg


    def recast(self):
        #Recast!
        self.starting_position = False
        self.tracking = None
        sleep(1)
        print('Recasting!')
        pyautogui.hotkey('shift', '9')
        sleep(4) # this prevents  self.starting_position from being set to an image of the bobber halfway being cast

    def moveCursorToTrackingPoint(self, tracking_point_clickpoints):
        clickpoint = tracking_point_clickpoints[0]
        random_mouse_move_duration = random.uniform(0.01,0.02)
        pyautogui.moveTo(clickpoint[0],clickpoint[1],duration=random_mouse_move_duration)
        random_sleep_time = random.uniform(0.01,0.2)
        random_sleep_time2 = random.uniform(1,2)
        sleep(random_sleep_time)
        pyautogui.rightClick() # cursor should be here already as we just moved above
        sleep(random_sleep_time)
        # left click 3 times to clear out items
        pyautogui.leftClick()
        sleep(random_sleep_time2)
        pyautogui.leftClick()
        sleep(random_sleep_time2)
        pyautogui.leftClick()
        sleep(random_sleep_time2)
        #reset starting position
        self.starting_position=False
        self.starting_time=time()
                
    def getStartingPosition(self):
        random_time_3 = random.uniform(3,4)
        #recast after no action
        if time() - self.starting_time > random_time_3:
            self.recast()
            self.starting_time = time()
            self.starting_position = False
            print('Recasting due to not finding target for > 3-4s!')
            return
        print('Acquiring starting position..')
        screenshot = self.wincap.get_screenshot()
        toFindBobberEye = self.bobber_eye.find(screenshot, self.weight, 'points')
        
        #look for Bobber Eye
        print('toFindBobberEye ='+str(toFindBobberEye))
        if toFindBobberEye.any():
            print('found BobberEye - setting self.starting_position')
            bobber_eye_clickpoints = self.bobber_eye.get_click_points(toFindBobberEye)
            clickpoint = bobber_eye_clickpoints[0]
            clickpoint_x = clickpoint[0]
            clickpoint_y = clickpoint[1]  # Assuming you want the last point
            self.starting_position = [clickpoint_x, clickpoint_y]
            print('self.starting_position is set to:', self.starting_position)
            self.starting_time = time()
            self.tracking = 'bobber eye'
            return
        else:
            print('No bobber_eye found.')
        #look for Feather
        screenshot = self.wincap.get_screenshot()
        toFindFeather = self.feather_pretty_far.find(screenshot, 0.79, 'points')
        if toFindFeather.any():
            feather_clickpoints = self.feather_pretty_far.get_click_points(toFindFeather)
            clickpoint = feather_clickpoints[0]
            clickpoint_x = clickpoint[0]
            clickpoint_y = clickpoint[1]  # Assuming you want the last point
            self.starting_position = [clickpoint_x, clickpoint_y]
            print('self.starting_position is set to:', self.starting_position)
            self.starting_time = time()
            self.tracking = 'feathers'
            return
        else:
            print('No feathers found.')





    def watchForMovement(self):

        if time() - self.starting_time > 20:
            self.recast()
            self.starting_time = time()
            print('Recasting due to not finding movement for >20s!')
            return

        if self.tracking == 'feathers':
            tracking_point = self.feather_pretty_far
        elif self.tracking == 'bobber eye':
            tracking_point = self.bobber_eye
        screenshot = self.wincap.get_screenshot()
        toFind = tracking_point.find(screenshot, self.weight, 'points')
        if toFind.any():
            tracking_point_clickpoints = tracking_point.get_click_points(toFind)
            clickpoint = tracking_point_clickpoints[0]
            clickpoint_x = clickpoint[0]
            clickpoint_y = clickpoint[1]
            print('self.starting_position[1]-clickpoint+y = '+str(self.starting_position[1] - clickpoint_y))
            print('it equals: '+str(self.starting_position[1] - clickpoint_y))
            if (self.starting_position[1] - clickpoint_y > 4 and self.starting_position[1] - clickpoint_y < 15) or (self.starting_position[1] - clickpoint_y < -4 and self.starting_position[1] - clickpoint_y > -15):
                print('feather moved more than 5 but less tahn 15 pixels on y axis')
                self.moveCursorToTrackingPoint(tracking_point_clickpoints)
                random_sleep_time = random.uniform(1,2)
                sleep(random_sleep_time)



    def exitApp(self):
        print('exiting app')
        sys.exit()

    def main(self):
        self.starting_time = time()
        sleep(2)#allows time to cast if started before casted out, preventing early detection of image as recast() is not called
        while(self.exitPlease == False):
            if (self.starting_position == False):
                self.getStartingPosition()
            else:
                self.watchForMovement()
            