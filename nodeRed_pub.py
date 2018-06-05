import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time
# import readchar #USED FOR SOME DEBUGGING STUFF
import numpy as np 

import matplotlib.pyplot as plt #use this for live plotting

import json



def nodeRed_listen_callback(client, userdata, msg):
    data = str(msg.payload, "utf-8")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("nodeRed_listen")
 
    client.message_callback_add("nodeRed_listen", nodeRed_listen_callback)
    


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


    while True:
    	# string = 'Hi'
    	# client.publish("nodeRed_test", string)
    	# print("published: " + string)
    	
    	temp_data = 'MAX31850' + '-'+ str(1) + ' Temp: ' +  str(72.5) 
    	client.publish('nodeRed_test', temp_data )
    	time.sleep(.5)
    	print("published: " + temp_data)
    	time.sleep(5)