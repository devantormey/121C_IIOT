
import paho.mqtt.client as mqtt #Paho MQTT is a lightweight mqtt library built for use with IOT Devices
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.connect(host="192.168.121.165", port=1883, keepalive=60)
    client.loop_start()

    temp = 26
    oldTime = time.time()
    currentTime = time.time()

    client.publish('testing',str(temp))
    print("published: " + str(temp) )


    while temp < 44:
    	currentTime = time.time()
    	if (currentTime - oldTime) > 60:
    		temp = temp + 1
    		client.publish('testing',str(temp))
    		print("published: " + str(temp) )
    		oldTime = time.time()