# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 22:46:08 2015

@author: Dong
"""

from StartButton import StartButton
from Motor import Motor
from MotorController import MotorController
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

d = 50 # mm

Forward=1 
turnRight=2 
turnLeft=3
Backward=0

N=0 
E=1 
S=2 
W=3

class MazeDiscovery:
    x = 6
    y = 6
    openList = []
    tempMaze = []
    maze = []
    visitedStack = []
    nextPosition = []
    gridInfo = [0,0,0,0]
    moveDirection = 0   # N=0 E=1 S=2 W=3
    motorDirection = 0  # N=0 E=1 S=2 W=3
    missingDistance = 0
    
    def __init__(self,  rover):  
        self.rover = rover

#      N E S W
#    N F R B L
#    E L F R B
#    S B L F R
#    W R B L F
#    
#    Backward=0 Forward=1 turnRight=2 turnLeft=3  from row number to column number
    

    def getTurnMode(self, motorDirection, moveDirection):
        
        turnList = [[1,2,0,3],
                    [3,1,2,0],
                    [0,3,1,2],
                    [2,0,3,1]]
        
        return turnList[motorDirection][moveDirection]

    def resetMotorDirection(self,turnMode):
         
        if turnMode ==1:
            return
            
        elif turnMode ==2:
            self.rover.turnRight()
            print "turnRight"
            sleep(2)
            self.motorDirection = (self.motorDirection+1)%4
        
        elif turnMode ==3:
            self.rover.turnLeft()
            print "turnLeft"
            sleep(2)
            self.motorDirection = (self.motorDirection-1)%4
            
        else:
            self.rover.turn180()
            print "turn180"
            sleep(2)
            self.motorDirection = (self.motorDirection+2)%4
         
    def moveToNext(self):
        for index in range (7):
            print "index : ",index
#            if index == 4:
#                self.setGridLeftRightInfo()
                
            self.moveRover2_5()
            
            if index == 6:
                self.setGridFrontInfo()  
                self.setGridLeftRightInfo()
                
    def  moveRover2_5(self):
#        Rightdistance1 = sc.readrightsensor()
#        Leftdistance1 = sc.readleftsensor()
#        print "Rightdistance1 : ", Rightdistance1
#        print "Leftdistance1 : ", Leftdistance1
#        self.rover.moveForwardmm(58.3, 5)        
#        sleep(3)
#        missingDistance = autoCorrection.autoCorrectAngle(Rightdistance1, Leftdistance1, 5.83)
        movelist = autoCorrection.missingDistanceAdjustment2(self.missingDistance, 5)
        self.rover.moveForwardmm(movelist[0], 5)
        sleep(4)
        if movelist[2] == turnLeft:
            self.rover.turnDegreesLeft(movelist[1])
            sleep(4)
        elif movelist[2] == turnRight:
            self.rover.turnDegreesRight(movelist[1])        
            sleep(4)
        self.missingDistance = autoCorrection.autoCorrectAngle2(5)

    def setGridLeftRightInfo(self):
        sensorRight = sc.readrightsensor()
        sensorLeft = sc.readleftsensor()
        
        self.gridInfo = [0,0,0,0]
           
        if sensorRight == 0 or sensorRight > 25:
           self.gridInfo.insert((self.motorDirection+1)%4, 1)
           self.gridInfo.pop((self.motorDirection+1)%4+1)
           
        self.gridInfo.insert((self.motorDirection+2)%4, 1)
        self.gridInfo.pop((self.motorDirection+2)%4+1)  
            
        if sensorLeft == 0 or sensorLeft > 25:
           self.gridInfo.insert((self.motorDirection+3)%4, 1)
           self.gridInfo.pop((self.motorDirection+3)%4+1)           

    def setGridFrontInfo(self):
        sensorFront = sc.readfrontsensor()
        
        if sensorFront == 0 or sensorFront > 15:
           self.gridInfo.insert(self.motorDirection, 1)
           self.gridInfo.pop(self.motorDirection+1)           

    def setOpenList(self):
    
        print self.gridInfo
        temporary = []
        temporary.append(self.y)
        temporary.append(self.x)        
        temporary.extend(self.gridInfo)
        self.tempMaze.append(temporary) 
            
        if self.gridInfo[0] == 1 and (self.motorDirection+2)%4 == 0:
            self.openList.append([self.y-1, self.x])

        elif self.gridInfo[1] == 1 and (self.motorDirection+2)%4 == 1:
            self.openList.append([self.y, self.x+1])   
            
        elif self.gridInfo[2] == 1 and (self.motorDirection+2)%4 == 2:
            self.openList.append([self.y+1, self.x]) 
                    
        elif self.gridInfo[3] == 1 and (self.motorDirection+2)%4 == 3:
            self.openList.append([self.y, self.x-1])

        if self.gridInfo[0] == 1 and (self.motorDirection+2)%4 != 0:
            self.openList.append([self.y-1, self.x])

        if self.gridInfo[1] == 1 and (self.motorDirection+2)%4 != 1:
            self.openList.append([self.y, self.x+1])   
            
        if self.gridInfo[2] == 1 and (self.motorDirection+2)%4 != 2:
            self.openList.append([self.y+1, self.x]) 
                    
        if self.gridInfo[3] == 1 and (self.motorDirection+2)%4 != 3:
            self.openList.append([self.y, self.x-1])

            
    def executeMoving(self):
        self.y = self.nextPosition[0]
        self.x = self.nextPosition[1]
        print "y : ",self.y
        print "x : ",self.x 
        turnMode = self.getTurnMode(self.motorDirection, self.moveDirection)
        self.resetMotorDirection(turnMode)        
        self.moveToNext() 
        
        if (self.nextPosition in self.visitedStack) != True:
            self.setOpenList()            
            self.visitedStack.append([self.y, self.x])        
        
    def mapping_maze(self):
        self.visitedStack.append([self.y, self.x])
        self.setGridLeftRightInfo()
        self.setGridFrontInfo()
        self.setOpenList()
        del self.openList[0]

        isRunning = 0
        while True:
            
            if startButton.getButton():
                isRunning = 1
                
            elif isRunning:
               
                while len(self.openList) != 0:   
                    print self.openList
                    self.nextPosition = self.openList.pop()            
                        
                    if self.nextPosition[0] < self.y:
                        self.moveDirection = N
                        self.executeMoving()
        
                    elif self.nextPosition[0] == self.y:
                    
                        if self.nextPosition[1] > self.x:
                            self.moveDirection = E
                            self.executeMoving()
        
                        elif self.nextPosition[1] < self.x:
                            self.moveDirection = W
                            print "moveDirection :",self.moveDirection
                            self.executeMoving()
        
                    elif self.nextPosition[0] > self.y:            
                        self.moveDirection = S
                        self.executeMoving()           
                isRunning = 0
                
    def sortRow(self, r):
        row = []
        for col in range (0, len(r)-1):
            for grid in r:        
                if grid[1] == col:        
                    row.insert(col, grid)
        return row

    def sort_maze(self):
        
#        maze = [[[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]],
#                [[],[],[],[],[],[],[]]]
        
        listY = []
        listX = []
        for grid in self.tempMaze:
            
            listY.append(grid[0])
            listX.append(grid[1])
            
        minY = min(listY)
        minX = min(listX)
        
        for grid in self.tempMaze:
            
            grid[0] = grid[0]-minY
            grid[1] = grid[1]-minX
            
        
        r0 = []
        r1 = []
        r2 = []
        r3 = []
        r4 = []
        r5 = []
        r6 = []

        for grid in self.tempMaze:
            
            if grid[0] == 0:
                r0.append(grid)
            elif grid[0] == 1:
                r1.append(grid)                
            elif grid[0] == 2:
                r2.append(grid)        
            elif grid[0] == 3:
                r3.append(grid)        
            elif grid[0] == 4:
                r4.append(grid)        
            elif grid[0] == 5:
                r5.append(grid)        
            elif grid[0] == 6:
                r6.append(grid)          
        
        row0 = self.sortRow(r0)
        row1 = self.sortRow(r1)        
        row2 = self.sortRow(r2)        
        row3 = self.sortRow(r3)
        row4 = self.sortRow(r4)
        row5 = self.sortRow(r5)
        row6 = self.sortRow(r6)

        self.maze.append(row0)
        self.maze.append(row1)
        self.maze.append(row2)
        self.maze.append(row3)
        self.maze.append(row4)
        self.maze.append(row5)
        self.maze.append(row6)
        
        def writeFil(self):
            
            # Open a file
            mazefile = open("mazefile.txt", "wb")
            for row in self.maze:
                for grid in row:
                    
                    mazefile.write(" ")
                    mazefile.write(grid[0])
                    mazefile.write(grid[1])
                    mazefile.write(" ")
                    mazefile.write(grid[2])
                    mazefile.write(grid[3])
                    mazefile.write(grid[4])
                    mazefile.write(grid[5])
            # Close opend file
            mazefile.close()



mazeDiscovery = MazeDiscovery(rover)

mazeDiscovery.mapping_maze()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            