from umqtt.simple import MQTTClient



client = MQTTClient('52dc166c-2de7-43c1-88ff-f80211c7a8f6', 
		'test.mosquitto.org') #where 52dc166c... is just some random number i generated to be the client ID.
client.connect()