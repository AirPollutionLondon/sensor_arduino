# create a string that has [sensorID, Latitude, Longitude, VOC(ppb), CO2(ppm)]

# import pymongo
import sensor_integration
import os

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)

for x in range(10):
    try: 
        sensor_integration.main();
    except SystemExit:
        print("in here")
        x+=1



