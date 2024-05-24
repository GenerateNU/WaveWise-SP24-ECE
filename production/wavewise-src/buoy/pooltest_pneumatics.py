from machine import Pin, ADC
from time import sleep

batterysense_pin=11
panelsense_pin=12
comp_pin = 9

ps = Pin(panelsense_pin, Pin.OUT) # compressor pin 
bs = Pin(batterysense_pin, Pin.OUT) # valve pin 
comp = Pin(comp_pin, Pin.IN)

while True:
    print("turn on battery sense -> valve")
    bs.value(1) 
    print(comp.value()) 
    sleep(5)

    print("turn off battery sense -> valve")
    bs.value(0)
    print(comp.value()) 
    sleep(5)

    # print("turn on panel sense -> pump")
    # ps.value(1) 
    # print(comp.value())
    # sleep(5)

    # print("turn off panel sense -> pump")
    # ps.value(0)
    # print(comp.value()) 
    # sleep(5)

    