# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 12:05:38 2015

@author: Dong
"""

import math
from time import sleep
 
class AutoCorrection:
    
    Rightdistance = 0
    Leftdistance = 0  
    count = 0
    def __init__(self, sc, rover):
        self.sc = sc
        self.rover = rover
        self.maxLength = 20
 
    def autoCorrectAngle(self, Rightdistance1, Leftdistance1, cm):
        angle = 0
        missingDistance = 0
        Rightdistance2 = self.sc.readrightsensor()        
        Leftdistance2 = self.sc.readleftsensor()
        print "Rightdistance2 : ", Rightdistance2
        print "Leftdistance2 : ", Leftdistance2        
        
        if (0 < Rightdistance1 < self.maxLength) and (0 < Rightdistance2 < self.maxLength):
            if Rightdistance1 > Rightdistance2:
                angle= math.degrees(math.atan2((Rightdistance1 - Rightdistance2), cm))
                print "autoCorrectAngle turnDegreesLeft : ", angle
                self.rover.turnDegreesLeft(math.floor(angle))
                sleep(2)
            elif Rightdistance1 < Rightdistance2:
                angle= math.degrees(math.atan2((Rightdistance2 - Rightdistance1), cm))
                print "autoCorrectAngle turnDegreesRight : ", angle
                self.rover.turnDegreesRight(math.floor(angle)) 
                sleep(2)
        elif (0 < Leftdistance1 < self.maxLength) and (0 < Leftdistance2 < self.maxLength):    
            if Leftdistance1 > Leftdistance2:
                angle= math.degrees(math.atan2((Leftdistance1 - Leftdistance2), cm))
                print "autoCorrectAngle turnDegreesRight : ", angle
                self.rover.turnDegreesRight(math.floor(angle))
                sleep(2)
            elif Leftdistance1 < Leftdistance2:
                angle= math.degrees(math.atan2((Leftdistance2 - Leftdistance1), cm))
                print "autoCorrectAngle turnDegreesLeft : ", angle
                self.rover.turnDegreesLeft(math.floor(angle))
                sleep(2)

        missingDistance = cm*(1-math.cos(math.radians(angle)))
        print "missingDistance : ", missingDistance
        return missingDistance
            
    def missingDistanceAdjustment(self, missingDistance, cm):
        
        Rightdistance = self.sc.readrightsensor()
        Leftdistance = self.sc.readleftsensor()
        angle = 0
        Forward=1
        turnRight=2 
        turnLeft=3
        returnDirection = 1
        Movedistance = 0
        movelist = []
        
        if (0 < Rightdistance < self.maxLength) and (0 < Leftdistance < self.maxLength):
            print "Rightdistance : ", Rightdistance
            print "Leftdistance : ", Leftdistance
            if Rightdistance > Leftdistance:        
                
                angle = math.degrees(math.atan2((Rightdistance - Leftdistance)/2, cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesRight : ", angle
                self.rover.turnDegreesRight(math.floor(angle))
                sleep(1)
                if angle != 0:
                    Movedistance = (Rightdistance - Leftdistance)/2/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
        
                returnDirection = turnLeft
            
            elif Leftdistance > Rightdistance:        
        
                angle = math.degrees(math.atan2((Leftdistance - Rightdistance)/2, cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesLeft : ", angle
                self.rover.turnDegreesLeft(math.floor(angle))
                sleep(1)
                if angle != 0:
                    Movedistance = (Leftdistance - Rightdistance)/2/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
                returnDirection = turnRight
        else:
                
            Movedistance = cm + missingDistance
            returnDirection = Forward
                
        movelist.append(Movedistance*10)
        movelist.append(angle)
        movelist.append(returnDirection)
        
        return movelist # cm*10 = mm

    def missingDistanceAdjustment2(self, missingDistance, cm):
        
        self.Rightdistance = self.sc.readrightsensor()
        self.Leftdistance = self.sc.readleftsensor()
        angle = 0
        Forward=1
        turnRight=2 
        turnLeft=3
        returnDirection = 1
        Movedistance = 0
        movelist = []
        
        if (0 < self.Rightdistance < self.maxLength) and ():
            print "Rightdistance : ", self.Rightdistance
            print "Leftdistance : ", self.Leftdistance
            if self.Rightdistance > 14 or self.Rightdistance == 14:        
                
                angle = math.degrees(math.atan2((self.Rightdistance - 14), cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesRight : ", angle
                self.rover.turnDegreesRight(math.floor(angle))
                sleep(2)
                if angle != 0:
                    Movedistance = (self.Rightdistance - 14)/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
        
                returnDirection = turnLeft
            
            elif self.Rightdistance < 14 or self.Rightdistance == 14:        
        
                angle = math.degrees(math.atan2((14 - self.Rightdistance), cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesLeft : ", angle
                self.rover.turnDegreesLeft(math.floor(angle))
                sleep(2)
                if angle != 0:
                    Movedistance = (14 - self.Rightdistance)/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
                    returnDirection = turnRight

        elif 0 < self.Leftdistance < self.maxLength:
            
            if self.Leftdistance > 14 or self.Leftdistance == 14:
                angle = math.degrees(math.atan2((self.Leftdistance - 14), cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesLeft : ", angle
                self.rover.turnDegreesLeft(math.floor(angle))
                sleep(2)
                if angle != 0:
                    Movedistance = (self.Leftdistance - 14)/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
        
                returnDirection = turnRight
            
            elif self.Leftdistance < 14 or self.Leftdistance == 14:        
        
                angle = math.degrees(math.atan2((14 - self.Leftdistance), cm + missingDistance))
                print "missingDistanceAdjustment turnDegreesRight : ", angle
                self.rover.turnDegreesRight(math.floor(angle))
                sleep(2)
                if angle != 0:
                    Movedistance = (14 - self.Leftdistance)/math.sin(math.radians(angle))
                    print "Movedistance : ", Movedistance
                else:
                        
                    Movedistance = cm + missingDistance
                    returnDirection = turnLeft
            
            
        else:
                
            Movedistance = cm + missingDistance
            returnDirection = Forward
                
        movelist.append(Movedistance*10)
        movelist.append(angle)
        movelist.append(returnDirection)
        
        if self.count == 1:
            return movelist # cm*10 = mm
        else:
            self.count += 1
            return [cm*10,0,1]
            

    def autoCorrectAngle2(self, cm):
        angle = 0
        missingDistance = 0
        Rightdistance1 = self.Rightdistance       
        Leftdistance1 = self.Leftdistance 
        Rightdistance2 = self.sc.readrightsensor()        
        Leftdistance2 = self.sc.readleftsensor()
        print "Rightdistance2 : ", Rightdistance2
        print "Leftdistance2 : ", Leftdistance2        
        
        if (0 < Rightdistance1 < self.maxLength) and (0 < Rightdistance2 < self.maxLength):
            if Rightdistance1 > Rightdistance2:
                angle= math.degrees(math.atan2((Rightdistance1 - Rightdistance2), cm))
#                print "autoCorrectAngle turnDegreesLeft : ", angle
#                self.rover.turnDegreesLeft(math.floor(angle))
#                sleep(2)
            elif Rightdistance1 < Rightdistance2:
                angle= math.degrees(math.atan2((Rightdistance2 - Rightdistance1), cm))
#                print "autoCorrectAngle turnDegreesRight : ", angle
#                self.rover.turnDegreesRight(math.floor(angle)) 
#                sleep(2)
        elif (0 < Leftdistance1 < self.maxLength) and (0 < Leftdistance2 < self.maxLength):    
            if Leftdistance1 > Leftdistance2:
                angle= math.degrees(math.atan2((Leftdistance1 - Leftdistance2), cm))
#                print "autoCorrectAngle turnDegreesRight : ", angle
#                self.rover.turnDegreesRight(math.floor(angle))
#                sleep(2)
            elif Leftdistance1 < Leftdistance2:
                angle= math.degrees(math.atan2((Leftdistance2 - Leftdistance1), cm))
#                print "autoCorrectAngle turnDegreesLeft : ", angle
#                self.rover.turnDegreesLeft(math.floor(angle))
#                sleep(2)

        missingDistance = cm*(1-math.cos(math.radians(angle)))
        print "missingDistance : ", missingDistance
        return missingDistance        
        
#def main():
#    auto = AutoCorrection(sc,mc)
#    auto.autocorrection()
#    
#if __name__ == '__main__':
#    main()