'''
- To receive query from end user and respond back result after collecting it from database.
- To create new nodes (internal and leaf) in best possible server and returning it to caller.
- To keep the content/object in CDN server using its key
'''
from stats import p
from stats import data
from stats import mutualScore
import client
######### File Content Structure for servermap, metadata and score  ################
#
# * Leaf Node or Internal Node (called 'entity' henceforth) will be represented
# by a tuple containing its serverID and name of the file it represents.
# Entities will be addressed using (ServerID, FileName)
#
# * Each server will have a serverID, whose mapping will be stored in servermap
# which will have server's IP, port to connect to and server's score(range 0-1).
# <serverID> <IP> <port> <max_storage_limit> <score>
# The score may be determined using network time, processing speed and other overheads
# This file will be mirrored in all the servers and updated anytime a change is seen.
#
# * metadata will contain information about current root and count of files 
# for each server for internal nodes and leaf nodes to allocate new name for files.
# First Line 	: <Number of servers>
# Second Line 	: <ServerID of server which has root> <Name of file which is the root>
# Third..n Line : <ServerID> <LeafCount> <NodeCount>
#
# * score will be used to collect statistics from query data. This can be used to learn
# patterns in query data and its response and accordingly migrate/rebuild the structure
# to optimize running time of queries.
#

numServer = 3
root = dict() # (serverID, fileName)
fileCount = dict() # { serverID:{'leafCount':lc, 'nodeCount':nc}, ...}
serverData = dict() # { serverID:{'IP': IP, 'port': port, 'maxStorageCapacity': maxCap, 'score': score}, ...}
cdnCount = 0

def readMetaData():
	global numServer, root, fileCount, cdnCount

	f = open('metadata','r')
	lines = f.readlines()
	numServer = int(lines[0].strip())
	rootinfo = lines[1].strip().split()
	root['serverID'] = rootinfo[0]
	root['fileName'] = rootinfo[1]

	for i in range(0, numServer):
		serverID, leafCount, nodeCount = lines[i+2].strip().split()
		fileCount[serverID] = {'leafCount': int(leafCount), 'nodeCount': int(nodeCount)}
	cdnCount += 1

	f.close()

def writeMetaData():
	global numServer, root, fileCount
	with open('metadata', 'w+') as f:
		f.write(str(numServer) + '\n')
		f.write(str(root['serverID']) + '\t' + root['fileName'] + '\n')
		for serverID, value in fileCount.iteritems():
			f.write(serverID + '\t' + str(value['leafCount']) + '\t' + str(value['nodeCount']) + '\n')

def updateRoot(serverID, fileName):
	global root
	root['serverID'] = serverID
	root['fileName'] = fileName
	writeMetaData()
	return 'SUCCESS'

def readServerData():
	global serverData, numServer
	f = open('servermap','r')
	for line in f.readlines():
		serverID, IP, port, maxCap, score = line.strip().split()
		score = float(score)
		maxCap = float(maxCap)
		port = int(port)
		serverData[serverID] = {'serverID': serverID, 'IP': IP, 'port': port, 'maxCap': maxCap, 'score': score}
	assert(len(serverData) == numServer)

def getBestServer(key):
	'''
	Returns the server id of the server based p-value of this key,
	server scores and server occupancy.
	'''
	global numServer, serverData, fileCount
	bestScore = 0
	bestServerID = ''
	for serverID, value in serverData.iteritems():
		occupancy = (fileCount[serverID]['leafCount'] + fileCount[serverID]['nodeCount'])*1.0 / value['maxCap'] / (2**20)
											# maxCap is in GB. fileSize is in KB. PageSize ~ 1
		mScore = mutualScore(value['score'], occupancy, p(key))
		if mScore > bestScore:
			bestScore = mScore
			bestServerID = serverID
	return bestServerID

def getNewLeaf(key):
	global fileCount
	serverID = getBestServer(key)
	fileCount[serverID]['leafCount']+=1
	newName = 'L'+('%09d'%fileCount[serverID]['leafCount'])
	result = {'serverID': serverID, 'fileName': newName}
	query = "CREATELEAF$"+result['fileName']
	client.request(result['serverID'], query)
	return result

def getNewNode(key):
	global fileCount
	serverID = getBestServer(key)
	fileCount[serverID]['nodeCount']+=1
	newName = 'N'+('%09d'%fileCount[serverID]['nodeCount'])
	query = "CREATENODE$"+result['fileName']
	client.request(result['serverID'], query)
	result = {'serverID': serverID, 'fileName': newName}
	return result

def saveContent(key, data):
	# TODO save the value in some CDN server
	return 'cdn'+str(cdnCount)
	

def insertInTree(key, data):
	ptr = saveContent(key, data)
	query = 'FINDLEAF$' + str(key) + '$' + root['fileName']
	response = client.request(root['serverID'], query)
	response = response.split('$')
	print response
	query = 'INSERTINLEAF$' + response[1] + '$' + str(key) + '$' + ptr
	response = client.request(response[0], query)
	print response



if __name__=='__main__':
	client.readServerMap()
	readMetaData()
	readServerData()
	# root = getNewLeaf(0.5)
	# root = getNewLeaf(2.0)
	# writeMetaData()
	# key = input('key: ')
	# data = raw_input('data: ')
	insertInTree(0.55, "data")
	# print 'Hola'
