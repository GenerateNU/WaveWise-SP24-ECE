from machine import Pin, ADC
from time import sleep

batterysense_pin=11
panelsense_pin=12
comp_pin = 9

bs = Pin(batterysense_pin, Pin.OUT) 
ps = Pin(panelsense_pin, Pin.OUT)
comp = Pin(comp_pin, Pin.IN)

while True:
    print(comp) 
    bs.value(1) 
    print(comp) 
    sleep(5)
    bs.value(0)
    ps.value(1) 
    print(comp)
    sleep(5) 
    ps.value(0)
    print(comp) 

    