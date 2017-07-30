'''
	Simple socket server using threads
'''

import socket
import sys
import time

HOST = ''	
PORT = 8888

i=0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
	server.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

#Start listening on socket
server.listen(1)
print 'Socket now listening'

#now keep talking with the client
conn, addr = server.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

while 1:
    try:
        if(i<255):
            i+=1
        else:
            i=0
        conn.send(str(i))
        time.sleep(0.5)
    except:
        print "Socket Lost"
        conn.close()
        server.close()
        break