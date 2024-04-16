from machine import Pin, ADC
from time import sleep

pressure_pin=27
pump_pin=13
valve_pin=22
saltwater_density=1025 #kg/m3
gravity=9.81 #m/s2


pressure = ADC(Pin(pressure_pin))
pump = Pin(pump_pin, Pin.OUT)
valve = Pin(valve_pin, Pin.OUT)
pressure_value=pressure.read_u16()

def get_depth(): 
    pressure_value=pressure.read_u16()
    return (1000* pressure_value)/saltwater_density*gravity

depth_input = int(input("Enter height in meters:"))
print(depth_input)
depth_input_low=depth_input-1
depth_input_high=depth_input+1
target_pressure= depth_input/(saltwater_density*gravity)

while True:
    depth= get_depth()
    if (depth_input_low)<depth<(depth_input_high):
        pump.off()
        valve.off()
        print('at depth')
    elif depth<depth_input_low:
        pump.on()
        print('pump on')
    elif depth>depth_input_high:
        valve.on()
        print('valve on')
    sleep(1)
    print (depth)
