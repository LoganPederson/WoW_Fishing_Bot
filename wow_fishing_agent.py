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
import logging


class FishingAgent:  

    def __init__(self, msg_queue):
        self.exitPlease = False
        self.wincap = WindowCapture()
        #self.bobber_eye = Vision('./Assets/bobber_eye.jpg')
        self.feather_pretty_far = Vision('./Assets/feathers_both_1080_prettyfar.jpg') #0.78 and >4s works medium at far and at night 
        #self.west_fall_feather = Vision('./Assets/bobber_eye.jpg')
        #self.west_fall_far = Vision('./Assets/WestFall_Far_1080.jpg')
        #self.west_fall_medium = Vision('./Assets/WestFall_Medium_Real_1080.jpg')
        #self.west_fall_close = Vision('./Assets/WestFall_Close_1080.jpg')
        self.feather_weight = 0.78
        self.starting_position = False
        self.weight = 0.7
        self.starting_time = 0
        self.tracking = None
        self.msg_queue = msg_queue
        #0.65 working well up close, not so great at distance using bobber_eye_eye.jpg

    def log_message(self, message):
        # Put the message onto the queue
        if self.msg_queue:
            self.msg_queue.put(message)
        pass

    def recast(self):
        #Recast!
        self.starting_position = False
        self.tracking = None
        sleep(1)
        self.log_message('Recasting!')
        pyautogui.hotkey('shift', '9')

    def moveCursorToTrackingPoint(self, tracking_point_clickpoints):
        clickpoint = tracking_point_clickpoints[0]
        random_mouse_move_duration = random.uniform(0.01,0.02)
        pyautogui.moveTo(clickpoint[0],clickpoint[1],duration=random_mouse_move_duration)
        random_sleep_time = random.uniform(0.01,0.2)
        random_sleep_time2 = random.uniform(0.4,1.4)
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
        random_time_3 = random.uniform(1,2)
        #recast after no action
        if time() - self.starting_time > random_time_3:
            self.recast()
            self.starting_time = time()
            self.starting_position = False
            self.log_message('Recasting due to not finding target for > 3-4s!')
            return
    
        self.log_message('Acquiring starting position..')



        #
        #look for WestFall Close
        #
        # screenshot = self.wincap.get_screenshot()
        # toFindWestfallClose = self.west_fall_close.find(screenshot, .88, 'points')
        # self.log_message('toFindWestfallClose ='+str(toFindWestfallClose))
        # if toFindWestfallClose.any():
        #     self.log_message('found BobberEye - setting self.starting_position')
        #     Westfall_clickpoints = self.west_fall_close.get_click_points(toFindWestfallClose)
        #     clickpoint = Westfall_clickpoints[0]
        #     clickpoint_x = clickpoint[0]
        #     clickpoint_y = clickpoint[1]  # Assuming you want the last point
        #     self.starting_position = [clickpoint_x, clickpoint_y]
        #     #self.log_message('self.starting_position is set to:'+str(self.starting_position_)
        #     self.starting_time = time()
        #     self.tracking = 'westfall close'
        #     return
        # else:
        #     self.log_message('No west_fall_close found.')
        # #
        # #look for WestFall Medium
        # #
        # screenshot = self.wincap.get_screenshot()
        # toFindWestfallmedium = self.west_fall_medium.find(screenshot, self.feather_weight, 'points')
        # #self.log_message('toFindWestfallClose ='+str(toFindWestfallmedium))
        # if toFindWestfallmedium.any():
        #     self.log_message('found BobberEye - setting self.starting_position')
        #     Westfall_clickpoints = self.west_fall_medium.get_click_points(toFindWestfallmedium)
        #     clickpoint = Westfall_clickpoints[0]
        #     clickpoint_x = clickpoint[0]
        #     clickpoint_y = clickpoint[1]  # Assuming you want the last point
        #     self.starting_position = [clickpoint_x, clickpoint_y]
        #     #self.log_message('self.starting_position is set to:', self.starting_position)
        #     self.starting_time = time()
        #     self.tracking = 'westfall medium'
        #     return
        # else:
        #     self.log_message('No west_fall_medium found.')
        #
        #look for WestFall Far
        #
        # screenshot = self.wincap.get_screenshot()
        # toFindWestfallFar = self.west_fall_far.find(screenshot, (self.feather_weight + 0.3), 'points')
        # #self.log_message('toFindWestfallFar ='+str(toFindWestfallFar))
        # if toFindWestfallFar.any():
        #     self.log_message('found BobberEye - setting self.starting_position')
        #     Westfall_clickpoints = self.west_fall_far.get_click_points(toFindWestfallFar)
        #     clickpoint = Westfall_clickpoints[0]
        #     clickpoint_x = clickpoint[0]
        #     clickpoint_y = clickpoint[1]  # Assuming you want the last point
        #     self.starting_position = [clickpoint_x, clickpoint_y]
        #     #self.log_message('self.starting_position is set to:', self.starting_position)
        #     self.starting_time = time()
        #     self.tracking = 'westfall far'
        #     return
        # else:
        #     self.log_message('No west_fall_Far found.')

        # #
        # #look for Westfall Feather
        # #
        # screenshot = self.wincap.get_screenshot()
        # toFindWestfallFeather = self.west_fall_feather.find(screenshot, self.feather_weight, 'points')
        # if toFindWestfallFeather.any():
        #     self.log_message('westfall feather found for starting pos')
        #     feather_clickpoints = self.west_fall_feather.get_click_points(toFindWestfallFeather)
        #     clickpoint = feather_clickpoints[0]
        #     clickpoint_x = clickpoint[0]
        #     clickpoint_y = clickpoint[1]  # Assuming you want the last point
        #     self.starting_position = [clickpoint_x, clickpoint_y]
        #     self.log_message('self.starting_position is set to:', self.starting_position)
        #     self.starting_time = time()
        #     self.tracking = 'westfallFeather'
        #     return
        # else:
        #     self.log_message('no Westfall feather Found')

        #
        #look for Feather
        #
        screenshot = self.wincap.get_screenshot()
        toFindFeather = self.feather_pretty_far.find(screenshot, self.feather_weight, 'points') #.79 works well for feathers pretty far
        if toFindFeather.any():
            self.log_message('found far feathers')
            feather_clickpoints = self.feather_pretty_far.get_click_points(toFindFeather)
            clickpoint = feather_clickpoints[0]
            clickpoint_x = clickpoint[0]
            clickpoint_y = clickpoint[1]  # Assuming you want the last point
            self.starting_position = [clickpoint_x, clickpoint_y]
            #self.log_message('self.starting_position is set to:', self.starting_position)
            self.starting_time = time()
            self.tracking = 'feathers far'
            return
        else:
            self.log_message('no far feather found')
        
        # #
        # #look for Bobber Eye
        # #
        # screenshot = self.wincap.get_screenshot()
        # toFindBobberEye = self.bobber_eye.find(screenshot, self.weight, 'points')
        # self.log_message('toFindBobberEye ='+str(toFindBobberEye))
        # if toFindBobberEye.any():
        #     self.log_message('found BobberEye - setting self.starting_position')
        #     bobber_eye_clickpoints = self.bobber_eye.get_click_points(toFindBobberEye)
        #     clickpoint = bobber_eye_clickpoints[0]
        #     clickpoint_x = clickpoint[0]
        #     clickpoint_y = clickpoint[1]  # Assuming you want the last point
        #     self.starting_position = [clickpoint_x, clickpoint_y]
        #     self.log_message('self.starting_position is set to:', self.starting_position)
        #     self.starting_time = time()
        #     self.tracking = 'bobber eye'
        #     return
        # else:
        #     self.log_message('No bobber_eye found.')







    def watchForMovement(self):

        if time() - self.starting_time > 20:
            self.recast()
            self.starting_time = time()
            self.log_message('Recasting due to not finding movement for >20s!')
            return

        if self.tracking == 'feathers':
            tracking_point = self.feather_pretty_far
        elif self.tracking == 'bobber eye':
            tracking_point = self.bobber_eye
        elif self.tracking == 'westfall far':
            tracking_point = self.west_fall_far
        elif self.tracking == 'westfall medium':
            tracking_point = self.west_fall_medium
        elif self.tracking == 'westfall close':
            tracking_point = self.west_fall_close
        elif self.tracking == 'westfallFeather':
            tracking_point = self.west_fall_feather
        elif self.tracking == 'feathers far':
            tracking_point = self.feather_pretty_far

        screenshot = self.wincap.get_screenshot() 
        toFind = tracking_point.find(screenshot, self.feather_weight, 'points') #adjust weight here
        if toFind.any():
            tracking_point_clickpoints = tracking_point.get_click_points(toFind)
            clickpoint = tracking_point_clickpoints[0]
            clickpoint_x = clickpoint[0]
            clickpoint_y = clickpoint[1]
            self.log_message('self.starting_position[1]-clickpoint+y = '+str(self.starting_position[1] - clickpoint_y))
            self.log_message('it equals: '+str(self.starting_position[1] - clickpoint_y))
            self.log_message('self.tracking == '+self.tracking)
            if (self.starting_position[1] - clickpoint_y > 5 and self.starting_position[1] - clickpoint_y < 20) or (self.starting_position[1] - clickpoint_y < -5 and self.starting_position[1] - clickpoint_y > -20):
                self.log_message('feather moved more than 4 but less than 20 pixels on y axis')
                self.moveCursorToTrackingPoint(tracking_point_clickpoints)
                random_sleep_time = random.uniform(1,2)
                sleep(random_sleep_time)



    def exitApp(self):
        self.log_message('exiting app')
        sys.exit()

    def main(self):
        self.starting_time = time()
        sleep(2)#allows time to cast if started before casted out, preventing early detection of image as recast() is not called
        self.recast()
        last_jump_time = time()
        while(self.exitPlease == False):
            loop_start_time = time()
            # Check if 10 minutes have passed since the last jump
            if loop_start_time - last_jump_time >= 600:
                pyautogui.press('space')  # Simulate spacebar press
                last_jump_time = loop_start_time  # Update the last jump time

            if (self.starting_position == False):
                self.getStartingPosition()
            else:
                self.watchForMovement()

            loop_end_time = time()  # Record the end time of the loop
            loop_duration = loop_end_time - loop_start_time  # Calculate the duration
            print(f"Loop Duration: {loop_duration:.4f} seconds")  # Print the duration
            