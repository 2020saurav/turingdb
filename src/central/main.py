'''
- To receive query from end user and respond back result after collecting it from database.
- To create new nodes (internal and leaf) in best possible server and returning it to caller.
- To keep the content/object in CDN server using its key
'''
from stats import p
from stats import data
from stats import mutualScore
import client
import random
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
# First Line    : <Number of servers>
# Second Line   : <ServerID of server which has root> <Name of file which is the root>
# Third..n Line : <ServerID> <LeafCount> <NodeCount>
#
# * score will be used to collect statistics from query data. This can be used to learn
# patterns in query data and its response and accordingly migrate/rebuild the structure
# to optimize running time of queries.

class Main:
	def __init__(self):
		self.numServer = 0
		self.root = dict() # (serverID, fileName)
		self.fileCount = dict() # { serverID:{'leafCount':lc, 'nodeCount':nc}, ...}
		self.serverData = dict() # { serverID:{'IP': IP, 'port': port, 'maxStorageCapacity': maxCap, 'score': score}, ...}
		self.cdnCount = 0
		self.readServerData()
		self.readMetaData()
		if self.root['serverID'] == 'SXX':
			self.root = self.getNewLeaf(0.5)
			self.writeMetaData()

	def readMetaData(self):
		f = open('metadata','r')
		lines = f.readlines()
		self.numServer = int(lines[0].strip())
		rootinfo = lines[1].strip().split()
		self.root['serverID'] = rootinfo[0]
		self.root['fileName'] = rootinfo[1]

		for i in range(0, self.numServer):
			serverID, leafCount, nodeCount = lines[i+2].strip().split()
			self.fileCount[serverID] = {'leafCount': int(leafCount), 'nodeCount': int(nodeCount)}
		self.cdnCount += 1
		f.close()

	def writeMetaData(self):
		with open('metadata', 'w+') as f:
			f.write(str(self.numServer) + '\n')
			f.write(str(self.root['serverID']) + '\t' + self.root['fileName'] + '\n')
			for serverID, value in self.fileCount.iteritems():
				f.write(serverID + '\t' + str(value['leafCount']) + '\t' + str(value['nodeCount']) + '\n')

	def updateRoot(self, serverID, fileName):
		self.root['serverID'] = serverID
		self.root['fileName'] = fileName
		self.writeMetaData()
		return 'SUCCESS'

	def readServerData(self):
		f = open('servermap','r')
		for line in f.readlines():
			serverID, IP, port, maxCap, score = line.strip().split()
			score = float(score)
			maxCap = float(maxCap)
			port = int(port)
			self.serverData[serverID] = {'serverID': serverID, 'IP': IP, 'port': port, 'maxCap': maxCap, 'score': score}
		# assert(len(serverData) == numServer)

	def getBestServer(self, key):
		'''
		Returns the server id of the server based p-value of this key,
		server scores and server occupancy.
		'''
		bestScore = 0
		bestServerID = ''
		for serverID, value in self.serverData.iteritems():
			occupancy = (self.fileCount[serverID]['leafCount'] + self.fileCount[serverID]['nodeCount'])*1.0 / value['maxCap'] / (2**20)
												# maxCap is in GB. fileSize is in KB. PageSize ~ 1
			mScore = mutualScore(value['score'], occupancy, p(key))
			if mScore > bestScore:
				bestScore = mScore
				bestServerID = serverID
		return 'S0' + str(random.randint(1,3))

	def getNewLeaf(self, key):
		self.readMetaData()
		self.readServerData()
		serverID = self.getBestServer(key)
		self.fileCount[serverID]['leafCount'] += 1
		newName = 'L'+('%09d'%self.fileCount[serverID]['leafCount'])
		result = {'serverID': serverID, 'fileName': newName}
		query = 'CREATELEAF$'+result['fileName']
		client.request(result['serverID'], query)
		self.writeMetaData()
		return result

	def getNewNode(self, key):
		self.readMetaData()
		self.readServerData()
		serverID = self.getBestServer(key)
		self.fileCount[serverID]['nodeCount']+=1
		newName = 'N'+('%09d'%self.fileCount[serverID]['nodeCount'])
		result = {'serverID': serverID, 'fileName': newName}
		query = 'CREATENODE$'+result['fileName']
		client.request(result['serverID'], query)
		self.writeMetaData()
		return result

	def saveContent(self, key, data):
		# TODO save the value in some CDN server
		return 'cdn'+str(self.cdnCount)


	def insertInTree(self, key, data):
		ptr = self.saveContent(key, data)
		query = 'FINDLEAF$' + str(key) + '$' + self.root['fileName']
		response = client.request(self.root['serverID'], query)
		response = response.split('$')
		query = 'INSERTINLEAF$' + response[1] + '$' + str(key) + '$' + ptr
		response = client.request(response[0], query)
		return 'SUCCESS'

	def windowQuery1(self, left, right):
		# left is included, right is not.
		query = 'FINDLEAF$' + str(left) + '$' + self.root['fileName']
		response = client.request(self.root['serverID'], query)
		response = response.split('$')
		query = 'WINDOWQUERY1$' + response[1] + '$' + str(left) + '$' + str(right)
		response = client.request(response[0], query)
		return response

	# if __name__=='__main__':
	#       # client.readServerMap()
	#       # readMetaData()
	#       # readServerData()
	#       root = getNewLeaf(0.5)
	#       writeMetaData()
	#       f = open('../small.in').readlines()
	#       for line in f:
	#               line = line.strip().split()
	#               insertInTree(float(line[0]), line[1])
	#       writeMetaData()
		# key = input('key: ')
		# data = raw_input('data: ')
		# insertInTree(0.55, 'data')
		# print 'Hola'
