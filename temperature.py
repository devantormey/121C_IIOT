import time
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20

class TemperatureSensor:
    """
    Represents a Temperature sensor
    """

    def __init__(self, pin, name):
        """
        Finds address of single DS18B20 on bus specified by `pin`
        :param pin: 1-Wire bus pin
        :type pin: int
        """
        self.name = name
        
        self.ds = DS18X20(OneWire(Pin(pin)))
        addrs = self.ds.scan()
        if not addrs:
            raise Exception('no DS18B20 found at bus on pin %d' % pin)
        # save what should be the only address found
        self.addr = addrs
    def read_temp(self, fahrenheit=True, addr_num=0):
        """
        Reads temperature from a DS18X20 thermocouple
        :param fahrenheit: Whether or not to return value in Fahrenheit
        :type fahrenheit: bool
        :return: Temperature
        :rtype: float
        """

        #First we gotta collect the addresses

        self.ds.convert_temp()
        time.sleep_ms(750)
        temp = self.ds.read_temp(self.addr[addr_num])
        if fahrenheit:
            return self.c_to_f(temp)
        return temp   
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
        self.ds.scan()

