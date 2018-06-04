# This code should listen over mqtt to the temperature data being produced by the esp32 device 

import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time
# import readchar #USED FOR SOME DEBUGGING STUFF
import numpy as np 
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
num_sens = 0
global temps
temps = [0]

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

    if data_list[2] != 'None':
        temp = float(data_list[2])
    else:
        temp = 0
    # temp_list['Sensor ' + device[-1]] =  temp
    if num_sens != 0:
        if len(temps) >= int(device[-1]): 
            temps[int(device[-1])] = temp
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
    # print("Callback Triggered, Number of sensors =  "+ str(num_sens))
    temps = [[] for i in range(0, num_sens)]

    for k in range(0,num_sens):
        if len(columns) < num_sens:
            if 'Sensor ' + str(k) not in columns:
                columns.append('Sensor ' + str(k))

def ping_callback(client, userdata, msg):
    global num_sens
    global columns 
    global temps
    # print("ping works!")
    data = str(msg.payload, "utf-8")
    # print(str(msg.payload, "utf-8"))
    if int(data) > num_sens:
        print("we've added a sensor, total number: "+ data)
        num_sens = int(data)
        temps.append(0)
    
    num_sens = int(data)   

    for k in range(0,num_sens):
        if len(columns) < num_sens:
            if 'Sensor ' + str(k) not in columns:
                columns.append('Sensor ' + str(k))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("sensor-setup")
    client.subscribe("sensor-data")
    client.subscribe("sensor-ping")
    client.message_callback_add("sensor-ping", ping_callback)
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
    client.connect(host="192.168.121.165", port=1883, keepalive=60)
    client.loop_start()
    # client.publish("setup-request",'Status Update Requested')


    try:
        print('collecting data...')
        while True:
        # print('Plotting data...')
            while i<5:
                time.sleep(1)

            print(temps)
            print(columns)
            i = 0;
            plt.clf()
            for k in range(0,num_sens):
                if temps[k] < 80.000 & temps[k] > 8.000:
                    plt.bar(columns[k],temps[k],color='g')
                    plt.pause(.5)

                if temps[k] > 80.000:
                    plt.bar(columns[k],temps[k],color='r')
                    plt.pause(.5)
                if temps[k] < 8.000:
                    plt.bar(columns[k],temps[k],color='r')
                    plt.pause(.5)

                # plt.show(False)
            plt.draw()
    except KeyboardInterrupt:
        print('interrupted!')
        
            # print(temp_list)
            # print(x)
            
            
