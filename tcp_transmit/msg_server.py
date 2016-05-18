from socket import *
from time import ctime
import time
import threading
import sys
import ctypes
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.

HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
friendtb = {}
usrdic=[]
offlinemsg = {}
socketary ={}
filetmp = {}
f = ''

def initial():
	global usrdic
	global friendtb
	global logoutmsg
	global filetmp
	usrdic = [
		{"username":"AAA", "password":"A11", "line":"offline"},
		{"username":"BBB", "password":"B11", "line":"offline"},
		{"username":"CCC", "password":"C11", "line":"offline"},
		{"username":"DDD", "password":"D11", "line":"offline"},
		{"username":"EEE", "password":"E11", "line":"offline"},
		{"username":"FFF", "password":"F11", "line":"offline"},
		{"username":"GGG", "password":"G11", "line":"offline"},
		{"username":"HHH", "password":"H11", "line":"offline"},
		{"username":"III", "password":"I11", "line":"offline"},
		{"username":"JJJ", "password":"J11", "line":"offline"}
	]
	for u in usrdic:
		friendtb[u['username']] = []
		offlinemsg[u['username']] = []
	for u in usrdic:
		filetmp[u['username']]={}
		for d in usrdic:
			filetmp[u['username']][d['username']] = ''

def addfriend(msg, uname):
	
	if msg[2] == uname:
		msg = ' Can not add yourself.\n'
		socketary[uname].send(msg.encode())
	else:
		# certify usr multi-add
		if friendtb[uname]== '':
			friendtb[uname].append(msg[2])
			msg = ' Add friend << ' + msg[2] + ' >>\n'
			f.write(uname + ':' + msg)
			f.flush()
			socketary[uname].send(msg.encode())
		else:
			flagrep = 0
			for i in range(0, len(friendtb[uname]), 1):
				if friendtb[uname][i] == msg[2]:
					flagrep = 1
					msg = ' The friend << ' + msg[2] + ' >> exist already.\n'
					socketary[uname].send(msg.encode())
					break
					
			if flagrep == 0:
				flagexist = 0
				# certify usr in usr dic.
				for d in usrdic:
					if d['username'] == msg[2]:
						flagexist = 1
						friendtb[uname].append(msg[2])
						msg = ' Add friend << ' + msg[2] + ' >>\n'
						f.write(uname + ':' + msg)
						f.flush()
						socketary[uname].send(msg.encode())
						break
				
				if flagexist == 0:
					msg = ' The user << '+ msg[2] +' >>does not exist.\n'
					socketary[uname].send(msg.encode())
				
def delfriend(msg, uname):
	flagrep = 0
	for i in range(0, len(friendtb[uname]), 1):
		if friendtb[uname][i] == msg[2]:
			flagrep = 1
			friendtb[uname].remove(msg[2])
			msg = ' Delete friend << ' + msg[2] + ' >> Done.\n'
			f.write(uname + ':' + msg)
			f.flush()
			socketary[uname].send(msg.encode())
			break
	if flagrep == 0:
		msg = ' The user << '+ msg[2] +' >>does not exist in your friend list.\n'
		socketary[uname].send(msg.encode())
				
def managefriend(msg, uname): # can input array 
	
	if msg[1] == 'add':
		if len(msg) != 3:
			msg = ' Command Error!\n'
			socketary[uname].send(msg.encode())
		else:
			addfriend(msg, uname)
			
	elif msg[1] == 'del':
		if len(msg) != 3:
			msg = ' Command Error!\n'
			socketary[uname].send(msg.encode())
		else:
			delfriend(msg, uname)
		
	elif msg[1] == 'list':
		if len(friendtb[uname]) == 0 :
			msg = ' No friend in the list\n'
			socketary[uname].send(msg.encode())
		else:
			flag = 0
			for d in range(0, len(friendtb[uname]), 1):
				for u in usrdic:
					msg = ''
					if friendtb[uname][d] == u['username']:
						if flag == 0:
							msg = '\b'
							flag = 1
						msg += '  ' + friendtb[uname][d] + ': ' + u['line'] + '\n' 
						socketary[uname].send(msg.encode())
						
	else:
		msg = ' friend [add/del] [usrname] : add/del friend\n'
		msg += '  friend list: show friend status\n'
		socketary[uname].send(msg.encode())


def managemsg(msg, uname):
	if len(msg) != 3:
		msg = ' usage: send [usr] [msg]\n'
		socketary[uname].send(msg.encode())
	else:
		matchwho = 0
		for who in usrdic:
			if who['username'] == msg[1]:
				matchwho = 1
				whoname = who['username']
				wholine = who['line']
		if matchwho == 0:
			msg = ' There is no this user.\n'
			socketary[uname].send(msg.encode())
		else:
			data = ' From ' + uname + ': ' + msg[2] + '\n'
			if wholine == 'online':
				socketary[whoname].send(data.encode())
				socketary[uname].send('\b'.encode())
			else:
				offlinemsg[whoname].append(data)
				socketary[uname].send('\b'.encode())

				
def managetalk(msg, uname):
	tousr = msg[1]
	while True:
		data = socketary[uname].recv(1024).decode()
		if data == 'quit':
			socketary[uname].send(' '.encode())
			break;
		ttt = '\b\b From ' + uname + ' : ' + data
		
		socketary[tousr].send(ttt.encode())
		
def managesendfile(msg, uname):
	
	f.write(uname + ': sendfile ' + msg[2] + ' to ' + msg[1])
	f.flush()
	# certify usr exist
	flagexist = 0

	for d in usrdic:
		if d['username'] == msg[1] and d['line'] == 'online':
			flagexist = 1
		elif d['username'] == msg[1] and d['line'] == 'offline':
			flagexist = 2
			
	if len(msg) != 3:
		sendmsg = ' Usage: sendfile [usr] [filename]\n'
		socketary[uname].send(sendmsg.encode())
	elif flagexist == 0:
		sendmsg = ' User << '+ msg[1] +' >> does not exist.\n'
		socketary[uname].send(sendmsg.encode())
	elif flagexist == 2:
		sendmsg = ' User << '+ msg[1] +' >> is offline.\n'
		socketary[uname].send(sendmsg.encode())
	
	elif msg[2] == 'yes': #uname: receiver ;  msg[1]: sender
		sendmsg = ' ' + uname + ' Accept.'
		socketary[msg[1]].send(sendmsg.encode())
		sendmsg = 'start ' + uname + ' ' + filetmp[msg[1]][uname]
		socketary[msg[1]].send(sendmsg.encode())
		sendmsg = 'receive ' + msg[1] + ' ' + filetmp[msg[1]][uname]
		socketary[uname].send(sendmsg.encode())
		time.sleep(3)
		
	elif msg[2] == 'no':
		sendmsg = ' Denied from ' + uname + '.'
		socketary[msg[1]].send(sendmsg.encode())
		
	else:
		filetmp[uname][msg[1]] = msg[2]
		filetmp[msg[1]][uname] = 'back'
		sendmsg = 'User ' + uname + ' : send a file ~ ' + msg[2] +' ~'
		socketary[msg[1]].send(sendmsg.encode())
		
def sendfilerun(msg, uname, data):
	cccc = data.split('sendfilerun ')
	tmp = msg[1] + ' '
	dddd = data.split(tmp)

	socketary[msg[1]].send(dddd[1].encode())
	if dddd[1] == 'EOF':
		time.sleep(4)
		sendmsg = 'Transimission Done!.\n'
		socketary[msg[1]].send(sendmsg.encode())
		socketary[uname].send(sendmsg.encode())
		
	#not send file
				
def chatthread(sock, uname):
	global usrdic
	
	while True:
		data = socketary[uname].recv(1024).decode()
		if data == '':
			continue
		msg = data.split(' ')
		if msg[0] == 'exit':
			f.write('User << ' + uname + ' >> Logout.\n')
			f.flush()
			sys.stdout.write('\b User << ' + uname + ' >> Logout.\n')
			socketary[uname].send('exit'.encode())
			for d in usrdic:
				if d['username'] == uname:
					d['line'] = 'offline'
					break
			socketary[uname].close()
			break
		elif msg[0] == 'send':
			managemsg(msg, uname)

		elif msg[0] == 'talk':
			managetalk(msg, uname)
			
		elif msg[0] == 'friend':
			managefriend(msg, uname)

		elif msg[0] == 'sendfile':
			managesendfile(msg, uname)
			
		elif msg[0] == 'sendfilerun':
			sendfilerun(msg, uname, data)
		else:
			msg = 'Error command!\n'
			socketary[uname].send(msg.encode())
			#print(usage)

def outputofflinemsg(uname):
	
	if len(offlinemsg[uname]) != 0:
		msg = 'Offline Message:\n'
		for i in range(0, len(offlinemsg[uname]), 1):
			msg += ' ' + offlinemsg[uname][i]
		socketary[uname].send(msg.encode())
		offlinemsg[uname] = []
		
def certifyID(sock):
	data = sock.recv(1024).decode()
	usrname, usrpwd = data.split('/')		
	flag = 0
	for d in usrdic:
		if d['username'] == usrname and d['password'] == usrpwd:
			flag = 1
			if d['line'] == 'online':
				sock.send("Double Login!!".encode())
				sock.close()
				f.write('User << '+ usrname +' >> Double Login.\n>')
				f.flush()
				sys.stdout.write('\b User << '+ usrname +' >> Double Login.\n>')
				
			else:
				sock.send("Welcome".encode())
				d['line'] = 'online'
				for d in usrdic:
					if d['username'] != usrname and d['line'] == 'online':
						sendmsg = usrname + ' online~\n'
						socketary[d['username']].send(sendmsg.encode())
				# add socket in ary
				socketary[usrname] = sock
				data = socketary[usrname].recv(1024).decode()
				if data == 'msg':
					outputofflinemsg(usrname)
				# create chat thread
				chat = threading.Thread(target = chatthread, args = (sock, usrname))
				chat.start()
				
				f.write('User << '+ usrname +' >> Login Successful.\n>')
				f.flush()
				sys.stdout.write('\b User << '+ usrname +' >> Login Successful.\n>')
				
		# match usrname, password error
		elif d['username'] == usrname and d['password'] != usrpwd:
			flag = 1
			sock.send(" Error Password!\n".encode())
			f.write('User << '+ usrname +' >> Login Error Password.\n>')
			f.flush()
			sys.stdout.write('\b User << '+ usrname +' >> Login Error Password.\n>')
			
	# no any match
	if flag == 0:
		sock.send(" Error Login!\n".encode())
		f.write('Login Error.\n>')
		f.flush()
		sys.stdout.write('\b  Login Error.\n>')


if __name__ == '__main__':
 	
	# initialize usr lsit
	initial()
	f = open('server.log', 'w')
	SerSock = socket(AF_INET, SOCK_STREAM)
	SerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse tcp
	SerSock.bind(ADDR)
	SerSock.listen(10)
	#SerSock.settimeout(100)
	
	# log_in
	while True:
		# certify identity
		Clisock, Cliaddr = SerSock.accept()
		certifyID(Clisock)		

	SerSock.close()
