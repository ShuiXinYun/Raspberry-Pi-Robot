import smbus,time,socket,sys

i2c_object=smbus.SMBus(1)
receiver_address = 0x08

while(1):
	try:
		i2c_object.write_byte(receiver_address,ord('A'))
		time.sleep(1)
		i2c_object.write_byte(receiver_address,ord('D'))
		time.sleep(1)
	except:
		print "Write data to Arduino Error"
