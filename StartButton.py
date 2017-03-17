# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 22:00:22 2015

@author: Dong
"""
from time import sleep
import RPi.GPIO as GPIO


class StartButton:
        
    def __init__(self, pin): # pin 15 = GPIO 3
       
        self.pin = pin 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
    def getButton(self):
        if GPIO.input(self.pin):
            GPIO.output(18, 1)
            sleep(1)
        else:
            GPIO.output(27, 1)
            sleep(1)
            GPIO.output(27, 0)
        return GPIO.input(self.pin)
            
           
    
    