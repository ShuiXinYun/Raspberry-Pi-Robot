# I2C write functions through SMBus implementation
# This work is licensed under a Creative Commons 
# Attribution-ShareAlike 4.0 International License.
# Created by Mike Ochtman. Find me on LinkedIn and drop me 
# a note if you found this helpful!

import smbus
import time

i2c = smbus.SMBus(1)
addr = 8 # address of the arduino I2C

##
##
##/* Interface Specification
##    Data in a table thus:
##      byte purpose
##      0: command
##      1: control
##     2-5: Current Temperature (read-only)
##     6-9: Current light level (read only)
##     10: Brightness for RED r/w
##     11: Brightness for GREEN r/w
##     12: Brightness for BLUE r/w
##
##     Commands:
##     Write with no command: Ignore
##     Read with no command: Return slave address
##     Command 0x81: read temperature. Integer returned, int(round(temp*100))
##     Command 0x82: read light level, Integer returned, int(round(lux*100))
##     Command 0x0A: Write three bytes to RGB
##     Command 0x0B: Write single byte brightness red;
##     Command 0x0C: Write single byte brightness green;
##     Command 0x0D: Write single byte brightness blue;
##     Command 0x90: read three bytes brightness RGB
##     Command 0x91: read single byte brightness red;
##     Command 0x92: read single byte brightness green;
##     Command 0x93: read single byte brightness blue;
##
##     All other values are ignored, no data returned.
##
##*/

RGB = [20,200,128]

temperature = 0
light_level = 0

i2c.write_quick(addr)
time.sleep(0.5)

print i2c.read_byte(addr)
time.sleep(0.5)

print i2c.read_word_data(addr,0x81)/100.0
time.sleep(0.5)

print i2c.read_word_data(addr,0x82)/100.0
time.sleep(0.5)

i2c.write_byte_data(addr, 0x0B, 12)
time.sleep(0.5)
print i2c.read_byte_data(addr, 0x91)
time.sleep(0.5)

i2c.write_byte_data(addr, 0x0C, 123)
time.sleep(0.5)
print i2c.read_byte_data(addr, 0x92)
time.sleep(0.5)
i2c.write_byte_data(addr, 0x0D, 234)
time.sleep(0.5)
print i2c.read_byte_data(addr, 0x93)
time.sleep(0.5)

print i2c.read_i2c_block_data(addr, 0x90, 3)
time.sleep(0.5)

i2c.write_i2c_block_data(addr, 0x0A, RGB)
time.sleep(0.5)

print i2c.read_i2c_block_data(addr, 0x90, 3)
time.sleep(0.5)

print i2c.read_i2c_block_data(addr, 0x10, 3)
time.sleep(0.5)


