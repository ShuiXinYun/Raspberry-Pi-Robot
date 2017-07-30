'''
Raspberry Pi as master, three Arduino as slave.
Arduino 0x08 controls two servos and two ultrasonicmodule HCSR-04, it send angle-distance data to rasp pi when requested.
'''
import smbus,time,socket,sys,tty,termios,threading

HOST = ''	
PORT = 8888
i2c_object=smbus.SMBus(1)
control_board_address=0x08
light_board_address=0x10
moveCMD = 'A'
Angle_Dist=[0,100]
processing_connect_trig=True
threads=[]

if processing_connect_trig:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket created'

	try:
		server.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Socket bind complete'
	server.listen(1)
	conn, addr = server.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def communication():
	if processing_connect_trig:
		try:
			Angle_Dist=i2c_object.read_i2c_block_data(control_board_address,0,2)
			print "Angle Dist is: ", Angle_Dist
			try:
				conn.sendall(str(Angle_Dist[0])+" "+str(Angle_Dist[1]))
			except:
				print "Connection to Processing Error"
		except:
			print "Data receive from Arduino Error"
		time.sleep(0.1)

def control(): 
	while(1):
		
		keyboard_input=getch()
		print "keyboard input is", keyboard_input+'\n'
		if(keyboard_input == 'w' or keyboard_input == 'W'):
			moveCMD='W'
		elif(keyboard_input == 's' or keyboard_input == 'S'):
			moveCMD='S'
		elif(keyboard_input == 'a' or keyboard_input == 'A'):
			moveCMD='A'
		elif(keyboard_input == 'd' or keyboard_input == 'D'):
			moveCMD='D'
			
		try:		
			i2c_object.write_byte(control_board_address,ord(moveCMD))
			print "moveCMD is: " + moveCMD
		except:
			print "Data write to Arduino Error"
		
		time.sleep(0.1)
		
threads_1=threading.Thread(target=communication)
threads.append(threads_1)
threads_2=threading.Thread(target=control)
threads.append(threads_2)

if __name__=='__main__':
	for t in threads:
		t.setDaemon(True)
		t.start()


