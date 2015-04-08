import socket
import sys
import pprint

serverDetails = dict()

def readServerMap():
	global serverDetails
	f = open('servermap','r')
	for line in f.readlines():
		serverID, IP, port, maxCap, score = line.strip().split()
		score = float(score)
		maxCap = float(maxCap)
		port = int(port)
		serverDetails[serverID] = {"IP": IP, "port": port, "maxCap": maxCap, "score": score}
	
def request(serverID, query):
	s = socket.socket()
	server = serverDetails[serverID]
	if server != None:
		s.connect((server['serverID'], server['port']))
		s.send(query)
		# wait for response
		responseLength = int(s.recv(100))
		# print responseLength
		response = s.recv(responseLength)
		# print response
		return response
	else:
		return "SERVER_NOT_FOUND"
	s.close()

# readServerMap()
# print serverDetails['S02']