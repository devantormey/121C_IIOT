def testing():
    import machine, onewire, MAX31850
    import network
    import boot
    import ubinascii
    from umqtt.simple import MQTTClient
    import time
    import json
    pin = 21
    # connect to the network and set network varialbe (just in case)
    # boot.connect()
    # sta_if = network.WLAN(network.STA_IF)


    #pull from the temperature.py script

    print("setting up sensor")
    from temperatureTC import TemperatureSensor

    t = TemperatureSensor(pin,'TC-1')
    num_sens = len(t.mx.scan())

    print('Found ' + str(num_sens) + ' Sensors. reading....')
    for k in range(0,num_sens):
        print('Temp of sensor ' + str(k) + ': ')
        temp = t.read_temp(addr_num = k) # use t.read_temp(False) to return Celsius
        print(temp)

    # connect to devans laptop IP
    print("connecting.... ")

    c =  MQTTClient("ESP32_dev", "192.168.121.165", port=1883, keepalive=60)
    c.connect()

    print("Done it should be connected")

    c.publish('sensor-setup', str(num_sens))

    # c.set_callback(sub_cb)
    # c.subscribe('setup-request')

    try:
        
        while True:
            for k in range(0,num_sens):
                # print("addr_num = " + str(k))
                payload = {
                'Sensor': 'MAX31850-' + str(k),
                'Temp': str(t.read_temp(addr_num = k))
                }

                temp_data = json.dumps(payload)
                c.publish('nodeRed_test', temp_data )
                time.sleep(.5)
                print("published: " + temp_data)
                time.sleep(5)
                current_time = time.time()



            
            if num_sens < len(t.mx.scan()):
                print("detected new sensor ")
                num_sens = len(t.mx.scan())
                addr_num = num_sens
                print("Now seeing " + str(num_sens) + " sensors")   
            c.publish('sensor-ping', str(num_sens))

    except KeyboardInterrupt:
        print('interrupted!')

    c.disconnect()