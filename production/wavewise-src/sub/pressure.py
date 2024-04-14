

from machine import Pin, ADC
from time import sleep

pressure = ADC(Pin(27))

while True:
  pot_value = pressure.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
  print(pot_value)
  sleep(1)