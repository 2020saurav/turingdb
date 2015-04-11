'''
Handler of central server to listen and respond to socket requests.
Network receieved queries will be parsed here,
and appropriate function in CentralServer.py will be called
'''
import socket
import sys
import time
import main

s = socket.socket()
s.bind(('',2020))
s.listen(10)

CentralServer = main.Main()

while True:
	sc, address = s.accept()
	# print address
	qlen = int(sc.recv(5))
	query = sc.recv(qlen)
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
		response = CentralServer.root['serverID'] + "$" + CentralServer.root['fileName']
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
		
	else:
		sc.send("5")
		sc.send("ERROR")
		
	sc.close()
s.close()