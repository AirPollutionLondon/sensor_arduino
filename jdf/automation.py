# create a string that has [sensorID, Latitude, Longitude, VOC(ppb), CO2(ppm)]

# import pymongo
from time import sleep
import sensor_integration
import os
h = .005
m = 60
s = 60

# sleep(100)
print("Launching Process...")
print("Performing sensor readings every 12 hours")
while(True):
    sensor_integration.main(True)
    sleep(h*m*s)

print("sleeping")
sleep(2)
sensor_integration.main(True)
print("waiting 10 secs before we do another read")
sleep(10)
sensor_integration.main(True)





