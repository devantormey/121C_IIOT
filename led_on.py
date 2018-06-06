import machine
import time
global led_pin 
led_pin = 13
pin = machine.Pin(led_pin, machine.Pin.OUT)

def led_on():
