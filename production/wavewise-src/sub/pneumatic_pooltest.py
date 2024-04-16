from machine import Pin, ADC
from time import sleep

pump_pin=13 #air in (up)
valve_pin=22 #air out (down)

pump = Pin(pump_pin, Pin.OUT)
valve = Pin(valve_pin, Pin.OUT)

valve.on()
sleep(10)
valve.off()

pump.on()
sleep(10)
pump.off()