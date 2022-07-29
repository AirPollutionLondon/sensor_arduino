# create a string that has [sensorID, Latitude, Longitude, VOC(ppb), CO2(ppm)]

from time import sleep
import sensor_integration
import os
import requests
import json

#should be run right after a reading is made (assumes that the method to create a json from a reading has been run)
def post_json():
    url='http://localhost:8080/api/sensorreading/upload'
    json_data=open('data_file.json')
    data=json.load(json_data)
    print(data)
    x=requests.post(url, json=data) # the actual post request
    print("json posted")

post_json()



