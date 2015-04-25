import socket
import sys
import pprint
import time 

serverDetails = dict()
centralServerID = 'S00'
networkCallCount = 0
delay = 0.005

def readServerMap():
	global serverDetails
	f = open('servermap','r')
	for line in f.readlines():
		serverID, IP, port, maxCap, score = line.strip().split()
		score = float(score)
		maxCap = float(maxCap)
		port = int(port)
		serverDetails[serverID] = {'serverID': serverID, 'IP': IP, 'port': port, 'maxCap': maxCap, 'score': score}

def request(serverID, query):
	time.sleep(delay) # to mimic network call
	global networkCallCount
	s = socket.socket()
	server = serverDetails[serverID]
	if server != None:
		s.connect((server['IP'], server['port']))
		networkCallCount += 1
		s.send(str('%05d'%len(query)))
		s.send(query)
		print "NETWORK CALL COUNT: ", networkCallCount
		# wait for response
		responseLength = int(s.recv(5))
		response = s.recv(responseLength)
        else:
		response = 'SERVER_NOT_FOUND'
        s.close()
        return response

readServerMap()
# print serverDetails['S02']
