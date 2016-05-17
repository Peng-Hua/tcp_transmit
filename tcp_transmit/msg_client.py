from socket import *
import sys
import threading
import getpass
import os
import time

HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
threads = []
tmp_file = ''

def send(sock, name):
	while True:
		data = input()
		msg = data.split(' ')
		if data == 'exit':
			sock.send(data.encode())
			break
		
		elif msg[0] == 'sendfile':
			if os.path.exists(msg[2]):
				sys.stdout.write('  Waitting ' + msg[1] + ' accept...\n')
				sock.send(data.encode())
			else:
				sys.stdout.write('\b  File does not exist.\n> ')
			
		elif msg[0] == 'yes' or msg[0] =='no':
			ddd = 'sendfile ' + tmp_file + ' ' + msg[0]
			sock.send(ddd.encode())
			if msg[0] =='no':
				sys.stdout.write('\n> ')
			
		else:
			sock.send(data.encode())	
		'''
			if os.path.exists(msg[2]):
				sock.send(data.encode())
				data  = sock.recv(1024).decode()
				print ('sdfdssfssssssssssssssssssssss')
				if data == 'yes':
					
				else:
					sys.stdout.write('\b  ' + msg[1] + ' Reject!\n ')
			else:
				sys.stdout.write('\b  File does not exist.\n> ')
		'''
		

def recv(sock, name):
	global tmp_file
	while True:
		data = sock.recv(1024).decode()
		msg = data.split(' ')
		if data == 'exit':
			sys.stdout.write('  ' + name + ' Logout!\n')
			sock.close()
			exit()
		
		elif msg[len(msg)-1] == '~':
			sys.stdout.write('\b ' + data + '\n ')
			sys.stdout.write('\b Accept file? <yes/no> : ')
			sys.stdout.flush()
			tmp_file = msg[1]

		elif msg[0] == 'start':
			
			sfile = open(msg[2], 'r')      
			filedata = sfile.read(1024)  
			if not filedata:
				break  
				
			while len(filedata) > 0:
				dddd = 'sendfilerun ' + msg[1] + ' ' + filedata
				intSent = sock.send(dddd.encode())   
				filedata = filedata[intSent:]   
			time.sleep(3)
			endoffile = 'sendfilerun ' + msg[1] + ' EOF'
			sock.send(endoffile.encode())
			
		elif msg[0] == 'receive':
			newfile = 'new_' + msg[2]
			f = open(newfile, 'w') 
			sys.stdout.write('\b ' + data + '\n')
			while True:
				dd = sock.recv(1024).decode()
				if dd == 'EOF': 
					f.flush()
					f.close()
					break  
				f.write(dd)
		else:
			sys.stdout.write('\b ' + data + '\n> ')	
			
		'''
			if req == 'yes':
				filename = msg[0].split('~')
				f = open(filename[1], 'wb') 				
				while True:   
					data = sock.recv(1024).decode()   
					if data == 'EOF':   
						break  
					f.write(data)   
				f.flush()
				f.close()
				sys.stdout.write('\b  Download finished.\n> ')
			else:
				continue
		'''
		

if __name__ == '__main__':

	CliSock = socket(AF_INET, SOCK_STREAM)
	CliSock.connect(ADDR)
	# login
	while True:
		username = input("Please input username: ")
		password = getpass.getpass("Please input password: ")
		login = username + "/" + password
		CliSock.send(login.encode())
		data = CliSock.recv(1024).decode()
		sys.stdout.write('\b  ' + data + ', ' + username + '\n> ')

		if data == "Welcome":
			CliSock.send("msg".encode())
			break
		else:
			CliSock.close()
			exit()

	chat = threading.Thread(target = send, args = (CliSock,username))
	threads.append(chat)
	chat = threading.Thread(target = recv, args = (CliSock,username))
	threads.append(chat)
	for i in range (len(threads)):
		threads[i].start()
	threads[0].join()


