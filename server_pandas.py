# This code should listen over mqtt to the temperature data being produced by the esp32 device 

import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time
import readchar #USED FOR SOME DEBUGGING STUFF
import pandas as pd
import numpy as np 
temp_list = pd.DataFrame() #create a pandas df
global columns 
columns = []
import matplotlib.pyplot as plt #use this for live plotting

global i #this indexes the messages (temperature values)
i = 0
global j #this indexes the messages (temperature values)
j = 0
global x
x = []
global num_sens
global temps

# global 


#Function that prints and stores some stuff whenever data is received
def tempsensor_callback(client, userdata, msg):
    #print("temp callback triggered")
    #had to make these global so i could actually see changes them in main(for plotting)
    global i 
    global j
    global x
    global num_sens
    global temps
    # global temp_list
    #print data packet
    print(str(msg.payload, "utf-8"))

    #seperate and store the actual integer for temperature
    data = str(msg.payload, "utf-8")
    data_list = []
    data_list = data.split()
    device = data_list[0]
    temp = float(data_list[2])
    # temp_list['Sensor ' + device[-1]] =  temp
    temps[int(device[-1])].append(temp)
    if (int(device[-1]) == 0):
        x.append(i)
        i = i + 1
    j = j + 1


    # print(temps) for debug

    
    

    # print(data_list) for debug

def setup_callback(client, userdata, msg):
    global num_sens
    global columns 
    global temps
    # global temp_list
    data = str(msg.payload, "utf-8")
    # print(str(msg.payload, "utf-8"))
    num_sens = int(data)
    temps = [[] for i in range(0, num_sens)]
    #  print(temps) for debug


    

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("sensor-data")
    print("subscribed to 'sensor-data' ")
    client.subscribe("sensor-setup")
    client.message_callback_add("sensor-data", tempsensor_callback)
    client.message_callback_add("sensor-setup", setup_callback)

    #subscribe to the temperature sensor

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="192.168.121.117", port=1883, keepalive=60)
    client.loop_start()

    try:
        print('collecting data...')
        while j<15:
            # print("delete this line")
            
            # plt.scatter(x1,temp_list1,c='b')
            # plt.pause(.5)
            # plt.show(False)
            # plt.draw()
            # print(len(x1))
            time.sleep(1)

        print('Plotting data...')

        #create a dataframe to be fille at the end
    
        # for k in range(0,num_sens):
        #     temp_list[ 'Sensor ' + str(k) ] = temps[k] 

        # print(temp_list)

        for k in range(0,num_sens):
            plt.scatter(x,temps[k])
       
        plt.show()

    except KeyboardInterrupt:
        print('interrupted!')
        
            # print(temp_list)
            # print(x)
            
            
