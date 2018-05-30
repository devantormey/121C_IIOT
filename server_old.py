# This code should listen over mqtt to the temperature data being produced by the esp32 device 

import paho.mqtt.client as mqtt
import time
import readchar
global temp_list
temp_list = []
import matplotlib.pyplot as plt
global i 
i = 0
global x 
x = []

def tempsensor_callback(client, userdata, msg):
    global i
    global temp_list
    global x
    print(str(msg.payload, "utf-8"))
    data = str(msg.payload, "utf-8")
    data_list = []
    data_list = data.split()
    device = data_list[1]
    temp = float(data_list[2])
    temp_list.append(temp)
    x.append(i)
    i = i + 1

    # print(data_list)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("sensor-data")
    client.message_callback_add("sensor-data", tempsensor_callback)

    #subscribe to the ultrasonic ranger topic here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    try:
        print("collecting data...")
        # print("press P to print")
        while True:
            # print("delete this line")
            input = readchar.readchar()
            if input == "p":
                plt.scatter(x,temp_list,c='b')
                plt.pause(.5)
                # plt.show(False)
                plt.draw()

            time.sleep(1)
            input = "k"
    except KeyboardInterrupt:
        print('interrupted!')
        
            # print(temp_list)
            # print(x)
            
            
