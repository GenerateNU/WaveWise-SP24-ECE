from machine import Pin, SPI
from time import sleep

# pins 
SPI_TX = 19
SPI_RX = 16
SPI_CSN = 17 
SPI_SCK = 18

STEP_PIN = 21
DIR_PIN = 20

# create SPI object
spi = SPI(0, baudrate=500000, polarity=0, phase=0, sck=Pin(SPI_SCK), mosi=Pin(SPI_TX), miso=Pin(SPI_RX), firstbit=SPI.MSB, bits=8)

chip_select = Pin(SPI_CSN, Pin.OUT) # chip select 
step_pin = Pin(STEP_PIN, Pin.OUT)
step_pin.value(0)
dir_pin = Pin(DIR_PIN, Pin.OUT)
dir_pin.value(0)

sleep(1) 

