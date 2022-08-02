# Written by Benoni Vainqueur, Meghna Gite, Declan Lowney, and Yuhong Zhao

from time import sleep
import sensor_integration
import os

# change h to 12 to have readings very 12 hours
h = .005
m = 60
s = 60

print("Launching Automator...")
print("Performing sensor readings every 12 hours")
while(True):
    sensor_integration.main(True)
    sleep(h*m*s)






