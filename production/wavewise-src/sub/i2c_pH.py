import machine
from time import sleep
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)

devices = i2c.scan()
for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))

i2c.writeto(0x63, 'R') # write 1 byte to slave device with address 0x63
sleep(1)
pH = i2c.readfrom(0x63, 7) # read 1 byte from slave device with address 0x63
# pH = []
# i2c.readfrom_into(0x63, pH) # read 1 byte and store in the buffer
print(pH)
i2c.writeto(0x64, 'R') # write 1 byte to slave device with address 0x63
sleep(1)
conductivity = i2c.readfrom(0x64, 7) # read 1 byte from slave device with address 0x63
print(conductivity)
# print(pH.decode())
# while True: 
    # print("reading from 0x68")
    # print(i2c.readfrom(0x68, 1)) # read 1 byte from slave device with address 0x68