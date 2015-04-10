'''
Handler of data server to listen and respond to socket requests.
Network receieved queries will be parsed here,
and appropriate function in bpt.py will be called
'''
import socket
import sys
import time
import bplustree as bpt

s = socket.socket()
s.bind(('',2021))
s.listen(10)

while True:
	sc, address = s.accept()
	# print address
	qlen = int(sc.recv(100))
	query = sc.recv(qlen)
	query = query.split('$')

	if query[0]=='FINDLEAF':
		key = float(query[1])
		node = query[2]
		response = bpt.findLeaf(key, node)
		sc.send(str(len(response)))
		sc.send(response)
	elif query[0]=='INSERTINLEAF':
		leafName = query[1]
		key = float(query[2])
		ptr = query[3] # will be object pointer.
		response = bpt.insertInLeaf(leafName, key, ptr)
		sc.send(str(len(response)))
		sc.send(response)
	else:
		print 'Unknown Query'
	sc.close()
s.close()