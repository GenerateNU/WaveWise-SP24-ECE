from machine import Pin, I2C
from time import sleep
 
comp_in=Pin(8, Pin.IN) # panel
valve_in=Pin(7, Pin.IN) # battery 

comp_out = Pin(13, Pin.OUT) 
valve_out = Pin(22, Pin.OUT)


while(True):
    # comp_in_val = comp_in.value() 
    # valve_in_val = valve_in.value() 
    # if (comp_in_val and valve_in_val): 
    #     comp_out.value(1) 
    #     valve_out.value(0)
    # else:     
    comp_out.value(comp_in.value())
    valve_out.value(valve_in.value())
    print("comp", comp_in.value(), "valve", valve_in.value())
    sleep(.1)
    # print(valve_in.value()) 