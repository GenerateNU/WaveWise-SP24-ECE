from machine import Pin
from time import sleep

panel_pin=10
battery_pin=11
pump_pin=13
valve_pin=22

pump = Pin(pump_pin, Pin.OUT)
valve = Pin(valve_pin, Pin.OUT)
panel_read= Pin(panel_pin, Pin.IN)
battery_read=Pin(battery_pin, Pin.IN)


while True:
    panel_read()
    battery_read()
    if panel_read.value == 1:
        pump.on()
    if battery_read.value == 1:
        valve.on()


    




