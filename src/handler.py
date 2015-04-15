'''
Handler of data server to listen and respond to socket requests.
Network receieved queries will be parsed here,
and appropriate function in bpt.py will be called
'''
from socket import *
import sys
import time
import bplustree
import thread

bpt = bplustree.BPT()

def handler(sc, address):
	res = sc.recv(5)
	print res,
	qlen = int(res)
	query = sc.recv(qlen)
	print query
	query = query.split('$')

	if query[0]=='FINDLEAF':
		key = float(query[1])
		fileName = query[2]
		response = bpt.findLeaf(key, fileName)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='INSERTINLEAF':
		# will be sent by central server
		leafName = query[1]
		key = float(query[2])
		ptr = query[3] # will be object pointer.
		response = bpt.insertInLeaf(leafName, key, ptr)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='INSERTINNODE':
		nodeName = query[1]
		key = float(query[2])
		serverID = query[3]
		fileName = query[4]
		ptr = {'serverID': serverID, 'fileName': fileName}
		response = bpt.insertInNode(nodeName, key, ptr)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='SAVELEAF':
		fileName = query[1]
		content = query[2]
		response = bpt.saveLeaf(fileName, content)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='SAVENODE':
		fileName = query[1]
		content = query[2]
		response = bpt.saveNode(fileName, content)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='CHANGELEFTPTR':
		fileName = query[1]
		ptr = {'serverID': query[2], 'fileName': query[3]}
		response = bpt.changeLeftPtr(fileName, ptr)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='CHANGEPARENT':
		fileName = query[1]
		ptr = {'serverID': query[2], 'fileName': query[3]}
		response = bpt.changeParent(fileName, ptr)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='CREATELEAF':
		fileName = query[1]
		response = bpt.createLeaf(fileName)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='CREATENODE':
		fileName = query[1]
		response = bpt.createNode(fileName)
		sc.send(str('%05d'%len(response)))
		sc.send(response)

	elif query[0]=='WINDOWQUERY1':
		fileName = query[1]
		left = float(query[2])
		right = float(query[3])
		response = bpt.windowQuery1(fileName, left, right)
		sc.send(str('%05d'%len(response)))
		sc.send(response)		

	else:
		sc.send('00005')
		sc.send('ERROR')
	sc.close()

if __name__=='__main__':
	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(('',2021))
	s.listen(10)
	while True:
		sc, address = s.accept()
		thread.start_new_thread(handler, (sc, address))
	s.close()
