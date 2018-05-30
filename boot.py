def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...boys')
        sta_if.active(True)
        sta_if.connect('121C', 'AdAstra17')
        print('success!')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

   


def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)

def sense():
    import machine, onewire, ds18x20
    import network
    import boot
    import ubinascii
    from umqtt.simple import MQTTClient
    import time
    pin = 6
    # connect to the network and set network varialbe (just in case)
    # boot.connect()
    # sta_if = network.WLAN(network.STA_IF)


    #pull from the temperature.py script

    print("setting up sensor")
    from temperature import TemperatureSensor
    t = TemperatureSensor(pin,'DS18B20-1')
    num_sens = len(t.ds.scan())

    print('Found ' + str(num_sens) + ' Sensors. reading....')
    for k in range(0,num_sens):
        print('Temp of sensor ' + str(k) + ': ')
        temp = t.read_temp(addr_num = k) # use t.read_temp(False) to return Celsius
        print(temp)

    # connect to devans laptop IP
    print("connecting.... ")

    c =  MQTTClient("ESP32_dev", "192.168.121.117", port=1883, keepalive=60)
    c.connect()

    print("Done it should be connected")
    c.publish('sensor-setup', str(num_sens))


    try:
        while True:
            for k in range(0,num_sens):
                print("Data To Published, Temperature is " + str(t.read_temp(addr_num = k)) + ' F' + ' From Sensor ' + str(k))
                c.publish('sensor-data', str(t.name) + '-'+ str(k) + ' Temp: ' +  str(t.read_temp(addr_num = k)) + ' F' )
                print("Done!")
                time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')

    c.disconnect()