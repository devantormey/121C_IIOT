# This code should listen over mqtt to the temperature data being produced by the esp32 device 

import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time
import readchar #USED FOR SOME DEBUGGING STUFF
import numpy as np  #create a pandas df
import matplotlib.pyplot as plt #use this for live plotting

global time_list
time_list = []
global temps
temps = []
import csv
global j
j = 0
global old_time
old_time = 0
# global 


#Function that prints and stores some stuff whenever data is received
def tempsensor_callback(client, userdata, msg):
    #print("temp callback triggered")
    #had to make these global so i could actually see changes them in main(for plotting)
    global j
    global temps
    global time_list
    global old_time
    # global temp_list
    #print data packet
    print(str(msg.payload, "utf-8"))

    #seperate and store the actual integer for temperature
    data = str(msg.payload, "utf-8")
    data_list = []
    data_list = data.split()
    # print(data_list)
    if int(data_list[0]) != old_time:
        temps.append(float(data_list[2]))
        time_list.append(int(data_list[0]))
        j = j + 1

    old_time = int(data_list[0])

    # print(temps)
    # print(time_list)




    # print(temps) for debug

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("sensor-data")
    client.message_callback_add("sensor-data", tempsensor_callback)


    #subscribe to the temperature sensor

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="192.168.121.165", port=1883, keepalive=60)
    client.loop_start()

    try:
        print('collecting data...')
        while j<3000:
            time.sleep(1)

        with open('heat_test2.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(time_list)
            wr.writerow(temps)
        myfile.close()
    except KeyboardInterrupt:

        print('interrupted!')
        
            
            
