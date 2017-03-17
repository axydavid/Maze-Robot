import time 
from sensor 
import getSensor 
import os 
#from motor import getMotorSpeed setMotorSpeed
enable = 0 
SV = 0 			#scaler variable 
maxCM = 25 		#CM treshhold for a hole 
width = 25 		#define the width of the hole 35-10 
speed = 0 
SC=1000
while True:		#def autoCorrect():  
LS = getSensor(2) 
RS = getSensor(1) 
speed = 100		#getMotorSpeed()
		
if RS > maxCM and LS > maxCM: 
LS = 1 RS = 1 
elif RS > maxCM: 
RS = width-LS 
elif LS > maxCM: 
LS = width-RS
SV = float(RS) / (LS) 
#setMotorSpeed(speed * SV) #set the motor speed, dependant on liu's code 
time.sleep(0.5)	 # 65 ms delay os.system('clear')
		
print LS 
print RS 
print speed 
print SV 
print speed * SV