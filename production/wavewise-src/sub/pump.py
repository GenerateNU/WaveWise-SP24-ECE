from machine import Pin
from time import sleep

pin = Pin(13, Pin.OUT)

# pin.on()
# while True:
#     pin.on()

while True:
    pin.toggle()
    sleep(10)