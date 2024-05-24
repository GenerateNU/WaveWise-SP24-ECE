from machine import Pin,UART
import time

uart = UART(0, baudrate=19200, bits = 8,parity = None,stop = 1, tx=Pin(0), rx=Pin(1))

# uart.init(bits=8, parity=None, stop=1)

led = Pin("LED", Pin.OUT)

print('setup')
while True:
    uart.write('AT\r')
    print('write')
    if uart.any(): 
        data = uart.read() 
        print(data)
        if data:
            led.toggle() 
    time.sleep(1)