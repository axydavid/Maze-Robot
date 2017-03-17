# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 15:00:37 2015

@author: Dong
"""
import math


RightMotorForward = 1
LeftMotorForward = 0
RightMotorBackward = 0
LeftMotorBackward = 1

microSteps16 = 16 #  microSteps/mm

turn1step = 16.5
turn90steps = 1490
turn180steps = 2980


class MotorController:

    def __init__(self, rightmotor, leftmotor):
        self.rightmotor = rightmotor
        self.leftmotor = leftmotor
        
    def runInit(self):
        self.rightmotor.runInit()
        self.leftmotor.runInit()

    def moveMotorInmm(self,mm):
        steps=int(math.floor((mm*microSteps16)))
        self.setPosition(steps)

    def moveForwardmm(self,mm,velocity): #to move forward with mm 
        self.rightmotor.resetPosition()
        self.leftmotor.resetPosition()
        self.rightmotor.setMotorParam(RightMotorForward,velocity)
        self.leftmotor.setMotorParam(LeftMotorForward,velocity)
        self.rightmotor.moveMotorInmm(mm)
        self.leftmotor.moveMotorInmm(mm)

    def moveBackwardmm(self,mm,velocity): #to move Backward with mm 
        self.rightmotor.resetPosition()
        self.leftmotor.resetPosition()
        self.rightmotor.setMotorParam(RightMotorBackward,velocity)
        self.leftmotor.setMotorParam(LeftMotorBackward,velocity)
        self.rightmotor.moveMotorInmm(mm)
        self.leftmotor.moveMotorInmm(mm)
    
    def turnRight(self): #turn 90 degrees to right
        self.rightmotor.resetPosition()
        self.leftmotor.resetPosition()
        self.rightmotor.setMotorParam(RightMotorBackward,5)
        self.leftmotor.setMotorParam(LeftMotorForward,5)
        self.rightmotor.setPosition(turn90steps)
        self.leftmotor.setPosition(turn90steps)
        
    def turnLeft(self): #turn 90 degrees to left
        self.leftmotor.resetPosition()
        self.rightmotor.resetPosition()
        self.leftmotor.setMotorParam(LeftMotorBackward,5)
        self.rightmotor.setMotorParam(RightMotorForward,5)
        self.leftmotor.setPosition(turn90steps)
        self.rightmotor.setPosition(turn90steps)

    def turn180(self): #turn 180 degrees to opposite
        self.leftmotor.resetPosition()
        self.rightmotor.resetPosition()
        self.leftmotor.setMotorParam(LeftMotorForward,5)
        self.rightmotor.setMotorParam(RightMotorBackward,5)
        self.leftmotor.setPosition(turn180steps)
        self.rightmotor.setPosition(turn180steps)

    def turnDegreesLeft(self,degrees): #turn specific degrees to left
        self.leftmotor.resetPosition()
        self.rightmotor.resetPosition()
        self.leftmotor.setMotorParam(LeftMotorBackward,5)
        self.rightmotor.setMotorParam(RightMotorForward,5)
        self.leftmotor.setPosition(int(math.floor(turn1step*degrees)))
        #return the largest integer value less than or equal to x
        self.rightmotor.setPosition(int(math.floor(turn1step*degrees)))

    def turnDegreesRight(self,degrees): #turn specific degrees to right
        self.leftmotor.resetPosition()
        self.rightmotor.resetPosition()
        self.leftmotor.setMotorParam(LeftMotorForward,0)
        self.rightmotor.setMotorParam(RightMotorBackward,0)
        self.leftmotor.setPosition(int(math.floor(turn1step*degrees)))
        self.rightmotor.setPosition(int(math.floor(turn1step*degrees)))

    def getFullStatus1(self): #print full status of motors
        print "Left Motor FullStatus1: \n", self.leftmotor.getFullStatus1()
        print "Right Motor FullStatus1: \n", self.rightmotor.getFullStatus1()

    def getFullStatus2(self):
        print "Left Motor FullStatus2: \n", self.leftmotor.getFullStatus2()
        print "Right Motor FullStatus2: \n", self.rightmotor.getFullStatus2()

    def setOtpParam(self):
        self.leftmotor.setOTPParam()
        self.rightmotor.setOTPParam()

    def softstop(self):
        self.rightmotor.softStop()
        self.leftmotor.softStop()

    def motorsRunning(self): #check the motors is running or not
        return self.leftmotor.isMotorRunning() and self.rightmotor.isMotorRunning()

