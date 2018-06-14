def set_temp( inTemp ):

    import machine, onewire, MAX31850
    import network
    import boot
    import ubinascii
    from umqtt.simple import MQTTClient
    import time
    import json


    # Choose the pins for the sensor and the control
    # set the mosfett pin as an output type

    pin_tc = 21

    pin_mos = 13

    mosPin = machine.Pin(pin_mos, machine.Pin.OUT)
    mosPin.value(0)
    heaterOn = False

    print("setting up sensor")
    from temperatureTC import TemperatureSensor
    t = TemperatureSensor(pin_tc,'TC-1')
    num_sens = len(t.mx.scan())
    k = 0 #This is 0 because we are testing and there is only one sensor

    temp = t.read_temp(addr_num = k)

    print('Intial Temperature of Sensor: ' + str(temp) )


    print("connecting.... to mqtt ")

    c =  MQTTClient("ESP32_dev", "192.168.121.165", port=1883, keepalive=60)
    c.connect()

    print("Done it should be connected")



    try:

    	while True:

            temp = t.read_temp(addr_num = k)

            print('Current Temperature: ' + str(temp) )

            c.publish('sensor-data',str( time.time() ) + ' , ' + str(temp) )
            
            if temp < inTemp:
    			mosPin.value(1)
    			heaterOn = True
            if temp > inTemp:
                mosPin.value(0)
                heaterOn = False

            print('Heater Status: ' + str(heaterOn))

    except KeyboardInterrupt:
        mosPin.value(0)
        print('Heating Stopped')


def listenTemp():
    import machine, onewire, MAX31850
    import network
    import boot
    import ubinascii
    from umqtt.simple import MQTTClient
    import time
    import json

     # Choose the pins for the sensor and the control
    # set the mosfett pin as an output type

    pin_tc = 21

    pin_mos = 13

    mosPin = machine.Pin(pin_mos, machine.Pin.OUT)
    mosPin.value(0)
    heaterOn = False

    global inTemp
    inTemp = 0

    global oldTime
    oldTime = 0
    print("setting up sensor")
    from temperatureTC import TemperatureSensor
    t = TemperatureSensor(pin_tc,'TC-1')
    num_sens = len(t.mx.scan())
    k = 0 #This is 0 because we are testing and there is only one sensor

    temp = t.read_temp(addr_num = k)

    print('Intial Temperature of Sensor: ' + str(temp) )



    def sub_cb(topic, msg):
        oldTime = time.time()
        global inTemp
        print("message received")
        print((topic, msg))
        data = msg.decode("utf-8")
        print("New Temperature detected: " + data)
        inTemp = int(data)

    print("connecting.... to mqtt ")

    c =  MQTTClient("ESP32_dev", "192.168.121.165", port=1883, keepalive=60)
    c.connect()
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"testing")

    print("Done it should be connected")

    print("waiting for message....")

    c.wait_msg()
    currentTime = time.time()

    print("Temp is: " + str(inTemp) + "of type: " + str( type(inTemp) ) )

    try:

        while True:

            temp = t.read_temp(addr_num = k)

            print('Current Temperature: ' + str(temp) )

            c.publish('sensor-data',str( time.time() ) + ' , ' + str(temp) )
               
            if temp < inTemp:
                mosPin.value(1)
                heaterOn = True
            if temp > inTemp:
                mosPin.value(0)
                heaterOn = False

            print('Heater Status: ' + str(heaterOn))
            print('Set Temperature is: '+ str(inTemp))
            c.check_msg()


        c.disconnect()
    except KeyboardInterrupt:
        mosPin.value(0)
        c.disconnect()
        print('Heating Stopped')
           
    







