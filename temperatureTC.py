import time
from machine import Pin
from onewire import OneWire
from MAX31850 import MAX31850

class TemperatureSensor:
    """
    Represents a Temperature sensor
    """

    def __init__(self, pin, name):
        """
        Finds address of single MAX31850 on bus specified by `pin`
        :param pin: 1-Wire bus pin
        :type pin: int
        """
        self.name = name
        
        self.mx = MAX31850(OneWire(Pin(pin)))
        addrs = self.mx.scan()
        if not addrs:
            raise Exception('no MAX31850 found at bus on pin %d' % pin)
        # save what should be the only address found
        self.addr = addrs
    def read_temp(self, fahrenheit=False, addr_num=0):
        """
        Reads temperature from a MAX31850 thermocouple
        :param fahrenheit: Whether or not to return value in Fahrenheit
        :type fahrenheit: bool
        :return: Temperature
        :rtype: float
        """
        # rescan for new sensors
        # addrs = self.ds.scan()
        # self.addr = addrs
        #First we gotta collect the addresses

        self.mx.convert_temp()
        time.sleep_ms(750)
        try:
            temp = self.mx.read_temp(self.addr[addr_num])
            if fahrenheit:
                return self.c_to_f(temp)
            return temp   
        except:
            addrs = self.mx.scan()
            self.addr = addrs
    @staticmethod
    def c_to_f(c):
        """
        Converts Celsius to Fahrenheit
        :param c: Temperature in Celsius
        :type c: float
        :return: Temperature in Fahrenheit
        :rtype: float
        """
        return (c * 1.8) + 32

    def return_addrs():
        #this should just print out available sensors id's
        self.mx.scan()

