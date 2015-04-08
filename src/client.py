import socket
import sys
import pprint

serverDetails = []

def readServerMap():
	global serverDetails
	f = open("servermap").readlines()
	for line in f:
		server = dict()
		line = line.strip().split(' ')
		server['serverID'] = line[0]
		server['IP'] = line[1]
		server['port'] = int(line[2])
		server['maxStorageLimit'] = float(line[3])
		server['score'] = float(line[4])
		serverDetails.append(server)

def getServerDetails(serverID):
	for server in serverDetails:
		if server['serverID'] == serverID:
			return server
	else:
		return None

def request(serverID, query):
	s = socket.socket()
	server = getServerDetails(serverID)
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
# print getServerDetails('S02')