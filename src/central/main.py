'''
- To receive query from end user and respond back result after collecting it from database.
- To create new nodes (internal and leaf) in best possible server and returning it to caller.
- To keep the content/object in CDN server using its key
'''
from stats import p
from stats import data

######### File Content Structure for servermap, metadata and score  ################
#
# * Leaf Node or Internal Node (called 'entity' henceforth) will be represented
# by a tuple containing its serverID and name of the file it represents.
# Entities will be addressed using (ServerID, FileName)
#
# * Each server will have a serverID, whose mapping will be stored in servermap
# which will have server's IP, port to connect to and server's score.
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

numServer = 0
root = [0,"filename"] # (serverID, filename)
fileCount = dict() # { serverID:{"leafCount":lc, "nodeCount":nc}, ...}

def readMetaData():
	global numServer, root, fileCount
	f = open('metadata','r')
	lines = f.readlines()
	numServer = int(lines[0].strip())
	root = lines[1].strip().split()
	root[0] = int(root[0])
	for i in range(0,numServer):
		serverID, leafCount, nodeCount = map(int,lines[i+2].strip().split())
		fileCount[serverID] = {"leafCount": leafCount, "nodeCount": nodeCount}
	f.close()

def writeMetaData():
	global numServer, root, fileCount
	with open("metadata", "w+") as f:
		f.write(str(numServer) + "\n")
		f.write(str(root[0]) + "\t" + root[1] + "\n")
		for serverID, value in fileCount.iteritems():
			f.write(str(serverID) + "\t" + str(value["leafCount"]) + "\t" + str(value["nodeCount"]) + "\n")

def getBestServer(key):
	'''
	Returns the server id of the server based p-value of this key,
	server scores and server occupancy.
	'''
	return 0

def getNewLeaf(key):
	global fileCount
	serverID = getBestServer(key)
	fileCount[serverID]["leafCount"]+=1
	newName = "L"+("%09"%fileCount[serverID]["leafCount"])
	# TODO actual file creation may not be needed
	return newName

def getNewLeaf(key):
	global fileCount
	serverID = getBestServer(key)
	fileCount[serverID]["nodeCount"]+=1
	newName = "L"+("%09"%fileCount[serverID]["nodeCount"])
	# TODO actual file creation may not be needed
	return newName

def saveContent(key, value):
	# save the value in some CDN server
	pass

# read contents from files servermap, metadata, scores.


# TODO Query handler

# TODO New Node Creator

# call stats.py when needed 

# TODO push content to CDN