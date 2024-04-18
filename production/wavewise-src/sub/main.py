from machine import Pin, I2C
from time import sleep, gmtime
sda=Pin(4)  # pull up?
scl=Pin(5)
readyint=Pin(11, Pin.IN)     # Ready/INT pin
i2c=I2C(0,sda=sda, scl=scl, freq=1000000)

UV_ADDR = 0x74  # default UV sensor address

# Control/Configuration register bank
_REG_ADDR_OSR    = 0x00 # Operational State Register
_REG_ADDR_AGEN   = 0x02 # API Generation Register
_REG_ADDR_CREG1  = 0x06 # Configuration Register 1
_REG_ADDR_CREG2  = 0x07 # Configuration Register 2
_REG_ADDR_CREG3  = 0x08 # Configuration Register 3
_REG_ADDR_BREAK  = 0x09 # Break Register
_REG_ADDR_EDGES  = 0x0A # Edges Register (for SYND mode)
_REG_ADDR_OPTREG = 0x0B # Option Register

# Output register bank (Measurement State) 
_REG_ADDR_STATUS   = 0x00 # Status register 
_REG_ADDR_TEMP     = 0x01 # Temperature measurement result
_REG_ADDR_MRES1    = 0x02 # Channel A measurement result
_REG_ADDR_MRES2    = 0x03 # Channel B measurement result
_REG_ADDR_MRES3    = 0x04 # Channel C measurement result
_REG_ADDR_OUTCONVL = 0x05 # Result of time conversion (lsb) 
_REG_ADDR_OUTCONVH = 0x06 # Result of time conversion (msb)

# OSR parameters
_OSR_SS     = 7     # 1= start of measurement (if DOS = measurement), 0 = stop
_OSR_PD     = 6     # 1= Power down on
_OSR_SW_RES = 3     # 1= software reset
_OSR_DOS_MSB = 2    # 010 = configuration, 011 = measurement
_OSR_DOS_LSB = 0
# OSR DOS modes
_OSR_CMODE = 0b010
_OSR_MMODE = 0b011
_OSR_NOP = 0b000

# CREG1 parameters
_CREG_GAIN_LSB = 4
_CREG_TIME_LSB = 0  # defines integration time of measurement
_GAIN_VAL = 0b0001
_INT_TIME_VAL = 0b0110

# CREG3 parameters
_CREG_CMD_MODE = 0b01   # CMD mode
_CREG_MMODE_LSB = 6

# BREAK parameters
_BREAK_VAL = 255    # break time

# Irradiance calculation parameters
_FSR_A = 312    # FSR in uW/cm2 for CREG1:TIME=6, gain=1024x
_FSR_B = 408
_FSR_C = 49
_NCLK_6 = 65536 # number of clock cycles within conv time for CREG1:TIME=6

devices = i2c.scan()
for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))

# Starts up in power-down state

# OSR (PD=0, power-down disabled --> Config state)
i2c.writeto_mem(UV_ADDR, _REG_ADDR_OSR, bytearray([_OSR_CMODE]), addrsize=8)   # write OSR - config state, power up
# CREG1 (gain, integration time)
i2c.writeto_mem(UV_ADDR, _REG_ADDR_CREG1, bytearray([_GAIN_VAL << _CREG_GAIN_LSB | _INT_TIME_VAL << _CREG_TIME_LSB]), addrsize=8)
# CREG2 (internal time measurement, divider disabled)
i2c.writeto_mem(UV_ADDR, _REG_ADDR_CREG2, bytearray([0b00000000]), addrsize=8)   # CREG2
# CREG3
i2c.writeto_mem(UV_ADDR, _REG_ADDR_CREG3, bytearray([_CREG_CMD_MODE << _CREG_MMODE_LSB]), addrsize=8)
# Break
i2c.writeto_mem(UV_ADDR, _REG_ADDR_BREAK, bytearray([_BREAK_VAL]), addrsize=8) # set max break time between conversions (for testing)

# Set to measurement mode --> M_IDLE state (PD = 0, MMODE = 1, SB = 0)
i2c.writeto_mem(UV_ADDR, _REG_ADDR_OSR, bytearray([_OSR_MMODE << _OSR_DOS_LSB]), addrsize=8)
while(True):
    # Set start bit SS=1, start new measurement
    i2c.writeto_mem(UV_ADDR, _REG_ADDR_OSR, bytearray([(1 << _OSR_SS) | (_OSR_MMODE << _OSR_DOS_LSB)]), addrsize=8)

    sleep(0.1)

    print("Measurement results")
    uva_bytes = i2c.readfrom_mem(UV_ADDR, _REG_ADDR_MRES1, 2, addrsize=8)
    uvb_bytes = i2c.readfrom_mem(UV_ADDR, _REG_ADDR_MRES2, 2, addrsize=8)
    uvc_bytes = i2c.readfrom_mem(UV_ADDR, _REG_ADDR_MRES3, 2, addrsize=8)
    uva_raw = (int.from_bytes(uva_bytes, "little"))
    uvb_raw = (int.from_bytes(uvb_bytes, "little"))
    uvc_raw = (int.from_bytes(uvc_bytes, "little"))
    
    print("Input light irradiance (Ee) in uW/cm2")
    uva_irradiance = _FSR_A/_NCLK_6 * uva_raw
    uvb_irradiance = _FSR_B/_NCLK_6 * uvb_raw
    uvc_irradiance = _FSR_C/_NCLK_6 * uvc_raw
    print(">UVA:", uva_irradiance)
    print(">UVB:",uvb_irradiance)
    print(">UVC:",uvc_irradiance)
# ------------------------------------------------------------------
print("Powering down")

# Stop measurement (SS = 0), in M_IDLE state
i2c.writeto_mem(UV_ADDR, _REG_ADDR_OSR, bytearray([(0 << _OSR_SS) | (_OSR_MMODE << _OSR_DOS_LSB)]), addrsize=8)
print(i2c.readfrom_mem(UV_ADDR, _REG_ADDR_OSR, 1, addrsize=8)) 

# Power down (PD = 1), in PDOWN state
i2c.writeto_mem(UV_ADDR, _REG_ADDR_OSR, bytearray([(1 << _OSR_PD) | (_OSR_MMODE << _OSR_DOS_LSB)]), addrsize=8)
print(i2c.readfrom_mem(UV_ADDR, _REG_ADDR_OSR, 1, addrsize=8)) 
# ------------------------------------------------------------------