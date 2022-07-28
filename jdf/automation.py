# create a string that has [sensorID, Latitude, Longitude, VOC(ppb), CO2(ppm)]

# import pymongo
from time import sleep
import sensor_integration
import os

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)

# for x in range(10):
#     try: 
#         sensor_integration.main(True);
#     except SystemExit:
#         print("in here")
#         # sensor_integration.main(True)
#         x+=1

sensor_integration.main(True)
print("sleeping")
sleep(2)
sensor_integration.main(True)
print("waiting 10 secs before we do another read")
sleep(10)
sensor_integration.main(True)





