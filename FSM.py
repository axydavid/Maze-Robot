# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 09:47:54 2015

@author: Dong
"""

from StartButton import StartButton
from Motor import Motor
from MotorController import MotorController
from Route import Route
from AutoCorrection import AutoCorrection
from SensorsController import SensorsController 
from time import sleep
startButton = StartButton(22)

rightmotor=Motor(0x60)
leftmotor=Motor(0x61)
rover=MotorController(rightmotor, leftmotor)
rover.getFullStatus1()
rover.getFullStatus2()
rover.moveForwardmm(1,5)
rover.runInit()
 
sc = SensorsController()
autoCorrection = AutoCorrection(sc, rover)

route=Route("testStraightLine.txt")
routeList=route.get_routeList()



d = 350 # mm
isRunning = 0
 
Forward=1 
turnRight=2 
turnLeft=3
Backward=0

N=0 
E=1 
S=2 
W=3

class FSM:
    
    moveDirection = N   # N=0 E=1 S=2 W=3
    roverDirection = N  # N=0 E=1 S=2 W=3

    def __init__(self,  rover):  
        self.rover = rover

#   to      N E S W
#
# from   N  F R B L
#        E  L F R B
#        S  B L F R
#        W  R B L F
#    
#    Backward=0 Forward=1 turnRight=2 turnLeft=3  from row number to column number
    

    def getTurnMode(self, roverDirection, moveDirection):
        
        turnList = [[1,2,0,3],
                    [3,1,2,0],
                    [0,3,1,2],
                    [2,0,3,1]]
        
        return turnList[roverDirection][moveDirection]

    def resetRoverDirection(self, turnMode):
         
        if turnMode == Forward:
            print "Forward"
            
        elif turnMode == turnRight:
            print "turnRight"
            self.rover.turnRight()
            sleep(2)
            self.roverDirection = (self.roverDirection+1)%4
        
        elif turnMode == turnLeft:
            print "turnLeft"
            self.rover.turnLeft()
            sleep(2)
            self.roverDirection = (self.roverDirection-1)%4
            
        else:
            print "turn180"
            self.rover.turn180()
            sleep(2)
            self.roverDirection = (self.roverDirection+2)%4
      
    def booleanAutoCorrect(self, pos1):
        
        if self.roverDirection == N:
            if (pos1[3] == 0 ) and ( pos1[5] == 0):
                return True

        elif self.roverDirection == S:
            if (pos1[3] == 0 ) and ( pos1[5] == 0):
                return True

        elif self.roverDirection == E:
            if (pos1[2] == 0 ) and ( pos1[4] == 0 ):
                return True

        elif self.roverDirection == W:
            if (pos1[2] == 0 ) and ( pos1[4] == 0 ):
                return True

        else:
            return False
     
    def  moveRover10_25(self):
        Rightdistance1 = sc.readrightsensor()
        Leftdistance1 = sc.readleftsensor()
        print "Rightdistance1 : ", Rightdistance1
        print "Leftdistance1 : ", Leftdistance1
        self.rover.moveForwardmm(100, 5)        
        sleep(2)
        missingDistance = autoCorrection.autoCorrectAngle(Rightdistance1, Leftdistance1, 10)
        movelist = autoCorrection.missingDistanceAdjustment(missingDistance, 25)
        self.rover.moveForwardmm(movelist[0], 5)
        sleep(5)
        if movelist[2] == turnLeft:
            self.rover.turnDegreesLeft(movelist[1])
            sleep(2)
        elif movelist[2] == turnRight:
            self.rover.turnDegreesRight(movelist[1])        
            sleep(2)

    def start(self):
        
        isRunning = 0
        while True:
            
            if startButton.getButton():
                isRunning = 1
                
            elif isRunning:
        
                for index in range(0, len(routeList)-1):
                    print "routeList index : ", index
                    pos1 = routeList[index]
                    pos2 = routeList[index+1]
                    
                    if pos2[0] < pos1[0]:  # check row number
                        
                        FSM.moveDirection = N  # move north
                        turnMode = FSM.getTurnMode(FSM.roverDirection, FSM.moveDirection)
                        FSM.resetRoverDirection(turnMode)
                        if FSM.booleanAutoCorrect(pos1):
                            FSM.moveRover10_25()
                            
#                        elif todo only one side wall:
#                            
                        else:
                            self.rover.moveForwardmm(350, 5)
                            sleep(5)
                    elif pos2[0] == pos1[0]:
                        
                        if pos2[1] > pos1[1]: # check column number
                            print "move east"
                            FSM.moveDirection = E # move east
                            turnMode = FSM.getTurnMode(FSM.roverDirection, FSM.moveDirection)
                            FSM.resetRoverDirection(turnMode)
                            if FSM.booleanAutoCorrect(pos1):
                                FSM.moveRover10_25()

#                           elif todo only one side wall:
#                            
                            else:
                                self.rover.moveForwardmm(350, 5)   
                                sleep(5)
                        elif pos2[1] < pos1[1]:
                            print "move west"
                            FSM.moveDirection = W # move west
                            turnMode = FSM.getTurnMode(FSM.roverDirection, FSM.moveDirection)
                            FSM.resetRoverDirection(turnMode)
                            if FSM.booleanAutoCorrect(pos1):
                                FSM.moveRover10_25()

#                           elif todo only one side wall:
#                            
                            else:
                                print "move west 350mm"
                                self.rover.moveForwardmm(350, 5)   
                                sleep(5)
                 
                    elif pos2[0] > pos1[0]:
                        
                        FSM.moveDirection = S # move south
                        turnMode = FSM.getTurnMode(FSM.roverDirection, FSM.moveDirection)
                        FSM.resetRoverDirection(turnMode)
                        if FSM.booleanAutoCorrect(pos1):
                            FSM.moveRover10_25()

#                        elif todo only one side wall:
#                            
                        else:
                            self.rover.moveForwardmm(350, 5)   
                            sleep(5)
                isRunning = 0
            
                        
        


FSM = FSM(rover)
FSM.start()




