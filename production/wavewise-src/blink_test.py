from machine import Pin
from time import sleep

pin = Pin("LED", Pin.OUT)
pin2 = Pin(28, Pin.OUT)

while True:
    pin.toggle()
    pin2.value(0)
    sleep(2)