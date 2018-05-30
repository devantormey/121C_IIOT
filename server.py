# This code should listen over mqtt to the temperature data being produced by the esp32 device 

import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time
import readchar #USED FOR SOME DEBUGGING STUFF
global temp_list1 #This just stores everytemperature reading (every 2-3 seconds) for plotting
temp_list1 = [] #make sure it's a list type for good measure
global temp_list2 #This just stores everytemperature reading (every 2-3 seconds) for plotting
temp_list2 = [] #make sure it's a list type for good measure
import matplotlib.pyplot as plt #use this for live plotting
global i #this indexes the messages (temperature values)
i = 0
global j #this indexes the messages (temperature values)
j = 0
global x1 
x1 = []
global x2
x2 = []


#Function that prints and stores some stuff whenever data is received
def tempsensor_callback(client, userdata, msg):
    #had to make these global so i could actually see changes them in main(for plotting)
    global i 
    global j
    global temp_list1
    global x1
    global x2
    #print data packet
    print(str(msg.payload, "utf-8"))

    #seperate and store the actual integer for temperature
    data = str(msg.payload, "utf-8")
    data_list = []
    data_list = data.split()
    device = data_list[0]
    temp = float(data_list[2])
    
    if device[-1] == "0":
        temp_list1.append(temp)
        x1.append(i)
        i = i + 1
    if device[-1] == "1":
        temp_list2.append(temp)
        x2.append(i)
        j = i + 1

    # print(data_list) for debug

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("sensor-data")
    client.message_callback_add("sensor-data", tempsensor_callback)

    #subscribe to the temperature sensor

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="192.168.121.117", port=8883, keepalive=60)
    client.loop_start()

    try:
        print('collecting data...')
        while (len(x1) < 20):
            # print("delete this line")
            
            # plt.scatter(x1,temp_list1,c='b')
            # plt.pause(.5)
            # # plt.show(False)
            # plt.draw()
            # print(len(x1))
            time.sleep(1)

        print('Plotting data...')
        plt.scatter(x1,temp_list1,c='b')
        plt.scatter(x2,temp_list2,c='g')
        plt.show()

    except KeyboardInterrupt:
        print('interrupted!')
        
            # print(temp_list)
            # print(x)
            
            
