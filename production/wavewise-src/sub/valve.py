from machine import Pin
from time import sleep

pin = Pin(22, Pin.OUT)


while True:
    pin.toggle()
    sleep(5)