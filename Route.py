# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 12:03:17 2015

@author: Dong
"""

class Route:
    
    def __init__(self, file_name):  # "route.txt"
        
        self.file_name = file_name
            
    def get_routeList(self):   
        
        count = 0        
        routeList = []
        route = open( self.file_name, "r")
        route.seek(0, 2)
        size = route.tell()
        print "Read String is : %i" % size
        route.seek(0, 0)
        
        while count < (size+1)/8:
            count+=1
            gridData = []
            count1 = 6
            
            while count1 != 0:
                str = route.read(1)
                if str.isspace() == False:    
                    count1-=1
                    strInt = int(str)
                    print "Read String is : %i" % strInt
                    gridData.append(strInt)
                    
            routeList.append(gridData)
             
        route.close()
        return routeList


# Test code:


#for gridData in Route("testStraightLine.txt").get_routeList():
#    
#    print gridData


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        