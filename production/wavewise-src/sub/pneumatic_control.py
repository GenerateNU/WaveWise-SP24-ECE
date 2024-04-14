from machine import Pin
from time import sleep
pressure_pin=27
pump_pin=13
valve_pin=22


pressure = ADC(Pin(pressure_pin))
pump = Pin(pump_pin, Pin.OUT)
valve = Pin(valve_pin, Pin.OUT)

depth_input = input("Enter height:")
target_pressure= depth_input/(water_density*grav)
while pressure < (target_pressure)
    valve.toggle()
    sleep(1)
    print(pressure)
else: 
    pump.toggle()
    sleep(1)

