from machine import Pin, SPI 
from time import sleep, sleep_us

# pins 
SPI_TX = 19
SPI_RX = 16
SPI_CSN = 17 
SPI_SCK = 18

STEP_PIN = 21
DIR_PIN = 20
SLEEP_PIN = 13 
FAULT_PIN = 15
RESET_PIN = 14
# motor gain 
GAIN_05 = 0b00 
GAIN_10 = 0b01 
GAIN_20 = 0b10
GAIN_40 = 0b11

# dead time in nanoseconds 
DTIME_400 = 0b00
DTIME_450 = 0b01
DTIME_650 = 0b10
DTIME_850 = 0b11

# motor modes 
STEP_001 = 0b0000 # full step
STEP_002 = 0b0001 # half step
STEP_004 = 0b0010 # quarter step
STEP_008 = 0b0011 # eighth step
STEP_016 = 0b0100 # sixteenth step
STEP_032 = 0b0101 # thirty-second step
STEP_064 = 0b0110 # sixty-fourth step
STEP_128 = 0b0111 # one hundred twenty-eighth step
STEP_256 = 0b1000 # two hundred fifty-sixth step

# register addresses 
CTRL_ADDR = 0x00
STATUS_ADDR = 0x07
def bit(n): return 1 << n
STATUS_CODE = {bit(0): "OTS", bit(1): "AOCP", bit(2): "BOCP", bit(3): "APDF", bit(4): "BPDF", bit(5): "UVLO", bit(6): "STD", bit(7): "STDLAT"}
STATUS_DESC = {bit(0): "Overtemperature shutdown", bit(1): "Channel A Overcurrent", bit(2): "Channel B Overcurrent", bit(3): "Channel A Pre-Driver Fault", bit(4): "Channel B Pre-Driver Fault", bit(5): "Under Voltage Lockout", bit(6): "Stall Detected", bit(7): "Latched Stall Detected"}

DEFAULT_VALUES = {  0x00 : [0xC, 0x10], # ctrl
                    0x01 : [0x1, 0xFF], # torque
                    0x02 : [0x0, 0x30], # off
                    0x03 : [0x0, 0x80], # blank 
                    0x04 : [0x011, 0x10], # decay 
                    0x05 : [0x0, 0x40], # stall
                    0x06 : [0xA, 0x59], # drive
                    0x07 : [0x0, 0x00], # status
}

# create SPI object
spi = SPI(0, baudrate=500000, polarity=0, phase=0, sck=Pin(SPI_SCK), mosi=Pin(SPI_TX), miso=Pin(SPI_RX), firstbit=SPI.MSB, bits=8)

chip_select = Pin(SPI_CSN, Pin.OUT) # chip select 
step_pin = Pin(STEP_PIN, Pin.OUT)
step_pin.value(0)
dir_pin = Pin(DIR_PIN, Pin.OUT)
sleep_pin = Pin(SLEEP_PIN, Pin.OUT)
fault_pin = Pin(FAULT_PIN, Pin.IN)
reset_pin = Pin(RESET_PIN, Pin.OUT)
dir_pin.value(0)

def ctrl_register(enable = 0, dir = 0, step = 0, mode = STEP_004, exstall = 0, gain = GAIN_05, dtime = DTIME_850): 
    chip_select.value(1)
    
    print("writing", bytearray([dtime << 2 | gain, exstall << 6 | mode  << 3 | step << 2 | dir << 1 | enable]).hex())
    spi.write(bytearray([(dtime << 2) | gain, (exstall << 6) | (mode  << 3) | (step << 2) | (dir << 1) | enable]))
    chip_select.value(0)
def write_register(addr, value): 
    chip_select.value(1)
    msg = [((0b0111 & addr) << 4) | value[0], value[1]]
    print([hex(msg[0]), hex(msg[1])], bytearray(msg))
    spi.write(bytearray(msg))
    # print(bytearray([((addr & 0b111) << 12) | ((value[0] << 8 | value[1]) & 0xFFF)]))
    chip_select.value(0)

def reset_settings(): 
    for addr, value in DEFAULT_VALUES.items(): 
        if(addr == CTRL_ADDR or addr == STATUS_ADDR):
            continue
        write_register(addr, value)
    write_register(CTRL_ADDR, DEFAULT_VALUES[CTRL_ADDR])
    write_register(STATUS_ADDR, DEFAULT_VALUES[STATUS_ADDR])
    
def read_register(addr):
    chip_select.value(1)
    # print("writing", bytearray([(bit(3) | addr) << 4, 0x00]))
    # spi.write(bytearray([(bit(3) | addr) << 4, 0x00]))
    data = spi.read(2, (bit(3) | addr) << 4)
    chip_select.value(0)
    return data
def read_status(): 
    data = read_register(STATUS_ADDR)
    print(bin(int.from_bytes(data, 'big')))
    for i in range(8): 
        if(int.from_bytes(data, 'big') & bit(i)): 
            print(STATUS_CODE[bit(i)], "-", STATUS_DESC[bit(i)])
    return data

def enable_motor(): 
    ctrl_register(enable=1)

def disable_motor(): 
    ctrl_register(enable=0)

def step_motor(dir = 0): 
    ctrl_register(enable=1, dir=dir, step=1)

def clear_status(): 
    chip_select.value(1)
    spi.write(bytearray([bit(3) | STATUS_ADDR, 0x00]))
    chip_select.value(0)
# while True:
#     chip_select.value(1)
#     sleep(.1)
#     chip_select.value(0)

sleep(1)


sleep_pin.value(1)
print("reset controller")
reset_pin.value(1)
sleep(.5) 
reset_pin.value(0)
print("status: ", read_register(STATUS_ADDR).hex(), "fault pin:", fault_pin.value())

reset_settings()
for i in range(8): 
    print("register: ", hex(i))
    print(read_register(i).hex())
print("fault pin:", fault_pin.value())

# ctrl_register()
# enable_motor()


for i in range(10): 
    ctrl_register(enable=0, dir=1, step=1)

    print("ctrl:",read_register(CTRL_ADDR).hex(), "status:", read_status().hex(), "fault pin:", fault_pin.value())
    sleep(1)
# # for i in range(10): 
# #     print("step high")
# #     step_pin.value(1) 
# #     sleep_us(300) 
# #     print("step low")
# #     step_pin.value(0)
# #     sleep_us(300) 

# for i in range(10): 
#     step_motor()
#     print("ctrl:",read_register(CTRL_ADDR).hex(), "status:", read_status().hex(), "fault pin:", fault_pin.value())
#     sleep(1)

print("disable motor")
disable_motor()
print(read_register(STATUS_ADDR).hex())

sleep_pin.value(0)