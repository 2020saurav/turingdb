'''
Handler of central server to listen and respond to socket requests.
Network receieved queries will be parsed here,
and appropriate function in CentralServer.py will be called
'''
from socket import *
import sys
import time
import main
import thread

CentralServer = main.Main()
delay = 0.001
port = 2020

def handler(sc, address):
	time.sleep(delay) # to mimic network delay
	res = sc.recv(5)
	print res,
	qlen = int(res)
	query = sc.recv(qlen)
	print query
	query = query.split('$')

	if query[0]=='NEWLEAF':
		key = float(query[1])
		newLeaf = CentralServer.getNewLeaf(key)
		response = newLeaf['serverID'] + '$' + newLeaf['fileName']
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='NEWNODE':
		key = float(query[1])
		newNode = CentralServer.getNewNode(key)
		response = newNode['serverID'] + '$' + newNode['fileName']
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='WHOISROOT':
		response = CentralServer.root['serverID'] + '$' + CentralServer.root['fileName']
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='CHANGEROOT':
		serverID = query[1]
		fileName = query[2]
		response = CentralServer.updateRoot(serverID, fileName)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='INSERT':
		key = float(query[1])
		data = query[2]
		response = CentralServer.insertInTree(key, data)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='WINDOW1':
		# Window 1 : Find Left -> This data server will complete whole task by traversing linked list
		left = float(query[1])
		right = float(query[2])
		response = CentralServer.windowQuery1(left, right)
		sc.send(str('%05d'%len(response)))
		sc.send(response)
		
	else:
		sc.send('00005')
		sc.send('ERROR')

	sc.close()

if __name__=='__main__':
	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(('', port))
	s.listen(10)
	while True:
		sc, address = s.accept()
		thread.start_new_thread(handler, (sc, address))
	s.close()