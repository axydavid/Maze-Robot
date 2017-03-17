# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 14:19:21 2015

@author: Dong
"""

import smbus
from time import sleep

class Sensor:

	def __init__(self, address):
		self.address = address
		self.bus = smbus.SMBus(1)

	def setCommand(self,command):
		self.bus.write_byte_data(self.address, 0, command)

	def setRange(self, range):
		self.bus.write_byte_data(self.address, 2, range)

	def setGain(self, gain):
		self.bus.write_byte_data(self.address, 1, gain)

	def range(self):
		#read register2 and 3 for range in cm
            rangeFull = 0            
            sleep(0.005)            
            range = self.bus.read_byte_data(self.address, 0)
            if range != 0xFF:                                    
                rangeH = self.bus.read_byte_data(self.address, 2)
                rangeL = self.bus.read_byte_data(self.address, 3)
                rangeFull = (rangeH << 8) | rangeL
            print "Sensor %X : %d cm"  % (self.address, rangeFull)
            return rangeFull
