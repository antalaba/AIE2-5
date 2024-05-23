import RPi.GPIO as GPIO
from time import sleep
import numpy as np


class Motor():
    def __init__(self, dir_pin, step_pin, step_revolution):
        self.DIR = dir_pin
        self.STEP = step_pin
        self.SPR = step_revolution


class Turret():
    def __init__(self): 
        self.step_revolution_motorH = int(7 * 3615)
        self.step_revolution_motorV= int(7 * 3200)
        self.dir_pin_H = 13
        self.step_pin_H = 26
        self.dir_pin_V = 19
        self.step_pin_v = 16
        self.horizontal_angle_target = 0
        self.vertical_angle_target = 0
        self.current_horiz_angle_turret = 0 
        self.current_vert_angle_turret = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.CW = 1
        self.CCW = 0
        self.delay = 0.0001  # change delay check the one on RspBrry
        self.motorHoriz = Motor(self.dir_pin_H, self.step_pin_H,self.step_revolution_motorH)
        self.motorVert=Motor(self.dir_pin_V,self.step_pin_v,self.step_revolution_motorV)

    def setup_motors(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motorHoriz.DIR, GPIO.OUT)
        GPIO.setup(self.motorHoriz.STEP, GPIO.OUT)
        GPIO.setup(self.motorVert.DIR, GPIO.OUT)
        GPIO.setup(self.motorVert.STEP, GPIO.OUT)

    def get_xyz(self,target_cord):
        self.x, self.y, self.z = target_cord

    def find_angle(self):  # find the horizontal angle with respect tothe origin
        distance_target = np.sqrt(self.x**2 + self.y**2 + self.z**2)

        self.vertical_angle_target = np.arcsin(self.z / distance_target)
        self.horizontal_angle_target = np.arctan2(self.x, self.y)
        
        self.vertical_angle_target = np.rad2deg(self.vertical_angle_target)
        self.horizontal_angle_target = np.rad2deg(self.horizontal_angle_target)
        
        if self.horizontal_angle_target <= 0:
                self.horizontal_angle_target = 360 + self.horizontal_angle_target
        self.horizontal_angle_target = 360 - self.horizontal_angle_target
       
        print(self.horizontal_angle_target)
        
    def move_horizontal_motor(self):
        angular_displacement = abs(self.current_horiz_angle_turret - self.horizontal_angle_target)
        steps_from_target = round((self.motorHoriz.SPR / 360) * angular_displacement)

        if (self.horizontal_angle_target > self.current_horiz_angle_turret):
            GPIO.output(self.motorHoriz.DIR, self.CW)  # If needed change self.CW or self.CCW

        elif (self.horizontal_angle_target <= self.current_horiz_angle_turret):
            GPIO.output(self.motorHoriz.DIR, self.CCW)  # If needed change self.CW or self.CCW

        for _ in range(steps_from_target):
            GPIO.output(self.motorHoriz.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.motorHoriz.STEP, GPIO.LOW)
            sleep(self.delay)

        self.current_horiz_angle_turret = self.horizontal_angle_target

    def move_vertical_motor(self):
        angular_displacement = abs(self.current_vert_angle_turret - self.vertical_angle_target)
        steps_from_target = round((self.motorVert.SPR / 360) * angular_displacement)

        if (self.vertical_angle_target > self.current_vert_angle_turret):
            GPIO.output(self.motorVert.DIR, self.CCW)  # If needed change self.CW or self.CCW

        elif (self.vertical_angle_target <= self.current_vert_angle_turret):
            GPIO.output(self.motorVert.DIR, self.CW)   # If needed change self.CW or self.CCW

        for _ in range(steps_from_target):
            GPIO.output(self.motorVert.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.motorVert.STEP, GPIO.LOW)
            sleep(self.delay)

        self.current_vert_angle_turret = self.vertical_angle_target


if __name__ == "__main__":
    pass
 
