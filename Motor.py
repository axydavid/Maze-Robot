# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 15:00:37 2015

@author: Dong
"""

import smbus
import time
import math


'class variables:'

#Motor commands:        ByteCode:    Description:
cmdGetFullStatus1     = 0x81       # to get a complete status of the circuit and of the stepper-motor
cmdGetFullStatus2     = 0xFC       # to get the 16 bits actual, target and 11 bits secure position
cmdGetOTPParam        = 0x82       # Returns OTP parameter
cmdGotoSecurePosition = 0x84       # Drives motor to secure position
cmdHardStop           = 0x85       # Immediate full stop
cmdResetPosition      = 0x86       # Sets actual position to zero
cmdResetToDefault     = 0x87       # Overwrites the chip RAM with OTP contents
cmdRunInit            = 0x88       # Reference Search
cmdSetMotorParam      = 0x89       # Sets motor parameter
cmdSetOTPParam        = 0x90       # Zaps the OTP memory
cmdSetPosition        = 0x8B       # Programmers a target and secure position
cmdSoftStop           = 0x8F       # Motor stopping with deceleration phase

microSteps16          = 19.76
stepModeByte          = 0x03       # AccShap=0,with v, stepMode=11, 16 microSteps
currentByte           = 0x92       #283mA/84mA
securePosBit          = 0xFF
Acc                   = 0x02        #Acc=1004FS/s2
class Motor:

    def __init__(self, devAddress):
        self.devAddress=devAddress
        self.bus = smbus.SMBus(1)

        '''to get a complete status of the circuit and of the stepper-motor'''
    def getFullStatus1(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus1, 9)
        return response

        '''to get the 16 bits actual, target position and 11 bits secure position'''
    def getFullStatus2(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus2, 9)
        return response
    
        '''to get the actual position of the stepper-motor'''
    def getPosition(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus2, 9)
        return (response[2] << 8) | response[3]

        '''to get the OTP (One-Time Programmable) parameters in the OPT memory'''
    def getOTPParam(self):
        return self.bus.write_byte(self.devAddress, cmdGetOTPParam)
    
        '''to move the motor to secure position'''
    def gotoSecurePosition(self):
        self.bus.write_byte(self.devAddress, cmdGotoSecurePosition)
        
    def hardStop(self):
        self.bus.write_byte(self.devAddress, cmdHardStop)
        
        '''to reset ActPos and TagPos registers'''
    def resetPosition(self):
        self.bus.write_byte(self.devAddress, cmdResetPosition)
        
        '''to reset the whole slave node into the initial state. ActPos value is copied into TagPos register'''
    def resetToDefault(self):
        self.bus.write_byte(self.devAddress, cmdResetToDefault)

        '''to initialize positioning of the motor by seeking the zero(or reference) position'''
    def runInit(self):
        byteCode = [0xFF, 0xFF, 0x80, 0x00, 0xf, 0x00, 0x10]
        self.bus.write_i2c_block_data(self.devAddress, cmdRunInit, byteCode)

        '''Set the stepper motor parameters in the RAM:

           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 7-4bit=Coil peak current value (Irun), 3-0bit=Coil hold current value (Ihold)
           Byte 4: 7-4bit=Max velocity(index 0-F), 3-0bit=Min velocity(index 0-F)
           Byte 5: 7-5bit=Secure position, bit4=Motion direction, 3-0bit=Acceleration
           Byte 6: 7-0bit=Secure position of the stepper motor
           Byte 7: bit4=Acceleration shape, Accshape=0 with Acceleration, 3-2bit=Stepmode
        '''
    def setMotorParam(self, direction, maxVelocity):
        vMaxvMin=maxVelocity << 4 | 1 <<0         
        status= securePosBit>>8 | direction<<4 | Acc 
        byteCode = [0xFF, 0xFF, currentByte, vMaxvMin, status, securePosBit, stepModeByte]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetMotorParam, byteCode)

    def setAcceleration(self, direction, acc):         
        status= securePosBit>>8 | direction<<4 | acc 
        byteCode = [0xFF, 0xFF, currentByte, 0x11, status, securePosBit, stepModeByte]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetMotorParam, byteCode)

        '''Zap the One-Time Programmable memory'''
    def setOTPParam(self, OTPAddress, Pbit):
        OTPAddress=0xF8 | OTPAddress
        byteCode = [0xFF, 0xFF, OTPAddress, Pbit]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetOTPParam, byteCode)

        '''Drive the motors to a given position in number of
           steps or microsteps:
        '''
    def setPosition(self,newPosition):
        posBitL=newPosition & 0xFF
        posBitH=newPosition >> 8
        byteCode = [0xFF, 0xFF, posBitH, posBitL]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetPosition, byteCode)

    def softStop(self):
        self.bus.write_byte(self.devAddress, cmdSoftStop)

    def moveMotorInmm(self,mm):
        microSteps=int(math.floor(mm*microSteps16))
        actPos= self.getPosition()
        if actPos != 0:
            self.setPosition(actPos+microSteps)
        else:
            self.setPosition(microSteps)

    def isMotorRunning(self):
        try:
            response = self.getFullStatus1()
            motionStatus = response[6]>>5
    
            if motionStatus != 0:
                return True
            else:
                return False
        except IOError:
            print ("IOError happened")
            self.isMotorRunning()

