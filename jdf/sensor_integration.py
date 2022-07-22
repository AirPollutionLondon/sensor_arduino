# this program will have the following capabilities

# establish the data structure that will store the values from the sensors
# this means it will add timestamps to the data that is retrieved from the arduino 

# this will also create some form of a file if it doesnt exist, and if it does, add additional data to the file. 
# top of the file will indicate when the last time the data was accessed. 
# this will also
# this program wi

#get lat/long from python 
#date and time 
#sensor data 


# Importing Libraries
# from asyncio.windows_events import NULL
from fileinput import filename
from genericpath import getctime
from operator import and_
import serial
import time
import os # imported to get the working directory 
from datetime import datetime, date
from enum import Enum
import serial.tools.list_ports
from os.path import exists
import math
import sys


SENSOR_EEPROM_ID = 0
SAMPLE_RATE = 10 # samples per minute
AGGREGATION_LIMIT = 50 # number of samples to take a data point of for that specific data point
ENABLED = True
FINAL_READ = 0
PORT_ID = '/dev/cu.usbmodem11101'
RPI_CONNECTED = False;
FILE_NAME = "SENSOR_DATA.txt"
global file_lines 




class Commands(Enum) :
    read = '_READ_'
    write = '_WRITE_'
    set = '_SET_'
    sample = '_SAMPLE_'
    rpi_send = '_RPI_SEND_'
    rpi_write = '_RPI_WRITE_'
    arduino_write = '_ARDUINO_WRITE_'


def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print("test: "+ p.device)
        if "Arduino" in p.description:
           
            print("This is an Arduino!")
        #print(p)
    # print("LOG: arduino connection successful")
    return arduino
   
def arduino_write(message):
    combined_msg = Commands.write + message
    if(arduino.is_open): 
        arduino.write(int(combined_msg,'utf-8'))
        return 1
    return -1;

def arduino_set(message):
    arduino_write(Commands.set + message)
    return 1;

# serial message will be: _WRITE_ _SET_ _SAMPLE_ (message) i.e write to the serial consle, set the sample as (message)
def arduino_sample(message):
    arduino_set(Commands.sample + message)
    return 1;

# reads a full line from the arduino serial console 
def arduino_read():
    time.sleep(.05)
    data = arduino.readline()
    return data

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(.1)
    data = arduino.readline()
    return data
    
    #this will wait for the arduino to send a message. 
    #the arduino must wait to continue until python sends its message back, confirming that it acknowledges the arduino.
#structure for communication to arduino:
# MODIFY [method name] [values]

# deliver sensor rate back to the arduino, modify how often we are polling by changing delay between reads.
# rate is in milliseconds. sensor_sample_config(500) is a sensor reading every 500 miliseconds 
def sensor_sample_config(rate):
    value = "SET _SAMPLE_" + rate 
    arduino.write(int(rate,'utf-8'))
    return 0;

# gets the eeprom_id from the serial line
def read_eeprom_id():
    current_line = arduino.read_all()
    if "SET _SENSORID_" in current_line :
       index = current_line.index("SENSORID ")
       SENSOR_EEPROM_ID = current_line[index:]

# this will initialize the process of retrieving a sensorID from the database if it does not have one.
def arduino_initalizer():
    SENSOR_EEPROM_ID = read_eeprom_id();
    if(SENSOR_EEPROM_ID == 0 or SENSOR_EEPROM_ID == NULL) :
        return 0
    else :
        return SENSOR_EEPROM_ID

# will get one serialized line. 
# def get_line():
#     return arduino.readall

# will turn the string into a object of type SensorReading
# TODO: Refactor code to not use magic number indices
def parser(serial_line):
    listed_values = serial_line.split() #timestamp.strftime("%Y-%m-%d %H:%M")
    time = datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    sensor_reading = SensorReading(str(formatted_time), int(listed_values[2]),int(listed_values[4]), 
                                                   int(listed_values[6]),int(listed_values[8]),
                                                   int(listed_values[10]),int(listed_values[12]),
                                                   int(listed_values[14]),int(listed_values[16]))
    return sensor_reading

def add_reading(sensor_reading):
    sensor_readings.append(sensor_reading)
    print("archived: " + sensor_reading.sensor_reading_to_string()) # LOG 
    return 1
  

# will aggregate the data points and take a average of the 20 samples in a minute, per say
def aggregator(num_samples = AGGREGATION_LIMIT):
    #maybe set arduino sample rate first.
    sum_voc = 0
    sum_co2 = 0
    sum_spm1 = 0
    sum_spm25 = 0
    sum_spm10 = 0
    sum_aec1 = 0
    sum_aec25 = 0
    sum_aec10 = 0

    # for i in num_samples:
    #    serial_line = arduino_read()
    #    add_reading(parser(serial_line))
    for s in sensor_readings :
        sum_voc+=int(s.voc)
        sum_co2+=int(s.co2)
        sum_spm1+=int(s.spm1)
        sum_spm25+=int(s.spm25)
        sum_spm10+=int(s.spm10)
        sum_aec1+=int(s.aec1)
        sum_aec25+=int(s.aec25)
        sum_aec10+=int(s.aec10)
    
    aggregated_reading = SensorReading(sensor_readings[num_samples-1].time,math.ceil(sum_voc /num_samples),
                            math.ceil(sum_co2/num_samples),
                            math.ceil(sum_spm1/num_samples),
                            math.ceil(sum_spm25/num_samples),
                            math.ceil(sum_spm10/num_samples),
                            math.ceil(sum_aec1/num_samples),
                            math.ceil(sum_aec25/num_samples),
                            math.ceil(sum_aec10/num_samples))
    return aggregated_reading
        
    print("sampled: " + num_samples + " times") 
    print("AVERAGE READING IS: " + aggregated_reading.sensor_reading_to_string())



def serial_no_generator():
    return 69
    

# will check if a file exists on the raspi. if it doesnt, create hte file, then go down init route
def file_handler(sensor_status, sensor_reading):
    file_exists = exists(FILE_NAME)
    if(file_exists): 
        with open(FILE_NAME, "r") as file: 
            data = file.readlines();  
            # updates last reading 
            data[0] = "Activated: " + str(sensor_status)+ "\n"
            data[2] = "Last Reading: " + sensor_reading.time +"\n"
        with open(FILE_NAME, "w") as file: 
            file.writelines(data)
            file.write(sensor_reading.sensor_reading_to_string()+"\n")
            file.close()

        # modify the first second and third line of file. 
        #   1. set activated to tue    
    else :
        f = open (FILE_NAME,"w")
        serial_no = serial_no_generator()
        f.write("Activated: "+ str(sensor_status)+ 
            "\nSerial Number(16-digit): "+ str(serial_no) + 
            "\nLast Reading: " + sensor_reading.time + "\n")
        f.write(sensor_reading.sensor_reading_to_string()+"\n")
        f.close()

    # The standard particulate matter mass concentration value refers to the mass concentration 
    # value obtained by density conversion of industrial metal particles as equivalent particles,
    #  and is suitable for use in industrial production workshops and the like. 
    # The concentration of particulate matter in the atmospheric environment is converted by the 
    # density of the main pollutants in the air as equivalent particles, and is suitable for ordinary
    #  indoor and outdoor atmospheric environments. So you can see that there are two sets of data above.
    # {"sensor num: ","PM1.0 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
    #                 "PM2.5 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
    #                 "PM10 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
    #                 "PM1.0 concentration(Atmospheric environment,unit:ug/m3): ",
    #                 "PM2.5 concentration(Atmospheric environment,unit:ug/m3): ",
    #                 "PM10 concentration(Atmospheric environment,unit:ug/m3): ",
    #                 };

class SensorReading:
    # VOC, CO2,
    #  pm1.0cf, pm2.5cf, pm10cf, 
  
    # spm = standard particulate matter 
    # aec = atmospheric environment concentration
    def __init__(self,time,voc,co2,spm1,spm25,spm10,aec1,aec25,aec10) :
        self.time = time
        self.voc = str(voc)
        self.co2 = str(co2)
        self.spm1 = str(spm1)
        self.spm25 = str(spm25)
        self.spm10 = str(spm10)
        self.aec1 = str(aec1)
        self.aec25 = str(aec25)
        self.aec10 = str(aec10)

    def sensor_reading_to_string(self):
        return("Time: "   + self.time +
             " VOC: "    + self.voc  + 
             " CO2: "    + self.co2 + 
             " SPM1.0: " + self.spm1 + 
             " SPM2.5: " + self.spm25  +  
             " SPM10: "  + self.spm10 + 
             " AEC1: "   + self.aec1  + 
             " AEC2.5: " + self.aec25 + 
             " AEC1.0: " + self.aec10)

    def set_sensor_time(self, new_time) :
        self.time = new_time
    
def arduino_connection(port_id=PORT_ID, rpi_connected = RPI_CONNECTED):
    #idk
    global arduino
    # if not rpi_connected
    arduino = serial.Serial(port_id, baudrate=115200, timeout=.1)
    
    while not rpi_connected:
        value = arduino_read().decode()
        valid = "successfully connected"
        waiting = "awaiting"
        if(len(value) > 0):
            # print("python: " + value + "\n")
            if(arduino.is_open and value != "\n"):
                print(value)
                if waiting in value:
                    print("beginning aggregation automatically.\n")
                    num = '199'
                    # value = write_read(num)
                    time.sleep(.1)
                    arduino.write(bytes(num, 'utf-8'))
                    time.sleep(1)
                elif valid in value:
                    print("_RPI_WRITE_" + value + " COMPLETE \n")
                    # print("finally")
                    rpi_connected = True  
                    return rpi_connected   
def main():
    print('starting main')
    
    RPI_CONNECTED = arduino_connection()
    # find_arduino_port();
    # arduino_connection

    # while True:
    #     # num = input("Enter a number: ") # Taking input from user
    #     # value = write_read('199')
    #     # bytes("TEST WRITe")
    #     arduino.write(bytes("TEST WRITE", 'utf-8'))
    #     data = arduino.readline()
    #     print(data) # printing the value

   #todo: 
   # do aggregation example. real. 
   # setup the file writing stuff
   # setup the process to turn on arduino when need be and turn it off when unnecessary 

# PROCESS: BEGIN DATA RETRIEVAL 

    setup_num_sensor_readings = 50
    actual_readings = 0
    global sensor_readings
    sensor_readings=[] 
    aggregated = False
    while True and not aggregated: 
        value = arduino_read().decode()
        if len(value) > 0 and value != '\n':
            if '_ARDUINO_WRITE_' in value :
                setup_num_sensor_readings-=1
                if(setup_num_sensor_readings < 0):
                    actual_readings +=1
                    s = parser(value)
                    add_reading(s);
                    if (actual_readings == AGGREGATION_LIMIT): 
                        ag_sensor_reading = aggregator()
                        aggregated = True
            else :
                print(value)
                
                # print(s.sensor_reading_to_string())
    print("aggregation complete. Values: " + ag_sensor_reading.sensor_reading_to_string())
    file_handler(False, ag_sensor_reading)
    arduino.close()
    # quit()

        
             
        
    # sys.exit()
    
    return 0




    
def __init__(none):
    cwd = os.getcwd()
    print("Current working directory: {0}".format(cwd))

    if(arduino_initalizer()): 
        return 0
    
    # Import the os module

# Get the current working directory


# Print the current working directory


# Print the type of the returned object
# print("os.getcwd() returns an object of type: {0}".format(type(cwd)))
    

main()


