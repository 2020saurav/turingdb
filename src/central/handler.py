'''
Handler of central server to listen and respond to socket requests.
Network receieved queries will be parsed here,
and appropriate function in main.py will be called
'''
import socket
import sys
import time
import main

s = socket.socket()
s.bind(('',2020))
s.listen(10)

while True:
	sc, address = s.accept()
	# print address
	qlen = int(sc.recv(100))
	query = sc.recv(qlen)
	query = query.split('$')

	if query[0]=='NEWLEAF':
		key = float(query[1])
		newLeaf = main.getNewLeaf(key)
		response = newLeaf['serverID'] + '$' + newLeaf['fileName']
		sc.send(str(len(response)))
		sc.send(response)

	elif query[0]=='NEWNODE':
		key = float(query[1])
		newNode = main.getNewNode(key)
		response = newNode['serverID'] + '$' + newNode['fileName']
		sc.send(str(len(response)))
		sc.send(response)

	elif query[0]=='WHOISROOT':
		response = main.root['serverID'] + "$" + main.root['fileName']
		sc.send(str(len(response)))
		sc.send(response)

	elif query[0]=='CHANGEROOT':
		serverID = query[1]
		fileName = query[2]
		response = main.updateRoot(serverID, fileName)
		sc.send(str(len(response)))
		sc.send(response)		

	else:
		sc.send("5")
		sc.send("ERROR")
		
	sc.close()
s.close()