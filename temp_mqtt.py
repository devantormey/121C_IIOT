
def sense():
	import machine, onewire, ds18x20
	import network
	import boot
	import ubinascii
	from umqtt.simple import MQTTClient
	import time

	# connect to the network and set network varialbe (just in case)
	# boot.connect()
	# sta_if = network.WLAN(network.STA_IF)


	#pull from the temperature.py script
	from temperature import TemperatureSensor
	t = TemperatureSensor(21)
	t.read_temp() # use t.read_temp(False) to return Celsius

	# connect to devans laptop IP
	c =  MQTTClient("ESP32_dev", '192.168.121.156')
	c.connect()


	try:
	    while True:
	        c.publish('sensor-data', str(t.read_temp()) )
	        time.sleep(3)
	except KeyboardInterrupt:
	    print('interrupted!')
	    


	


	c.disconnect()