# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 14:28:45 2015

@author: Dong
"""


from Sensor import Sensor

frontSensor=0x70
leftSensor=0x71
rightSensor=0x73
Range=0x0E # 70cm
Gain= 0x06
cm=0x51

class SensorsController:
    def __init__(self):
        self.frontsensor=Sensor(frontSensor)
        self.rightsensor=Sensor(rightSensor)
        self.leftsensor=Sensor(leftSensor)
        
    def readleftsensor(self):
        self.leftsensor.setGain(Gain)
        self.leftsensor.setRange(Range)
        self.leftsensor.setCommand(cm)
        range = self.leftsensor.range()

        return range

    def readrightsensor(self):
        self.rightsensor.setGain(Gain)
        self.rightsensor.setRange(Range)
        self.rightsensor.setCommand(cm)
        range = self.rightsensor.range()
  
        return range

    def readfrontsensor(self):
        self.frontsensor.setGain(Gain)
        self.frontsensor.setRange(Range)
        self.frontsensor.setCommand(cm)        
        range = self.frontsensor.range()

        return range    
 


     
     
