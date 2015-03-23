'''
- To receive query from end user and respond back result after collecting it from database.
- To create new nodes (internal and leaf) in best possible server and returning it to caller.
- To keep the content/object in CDN server using its key
'''

# Nodes will be addressed using (ServerID, FileName)
numServer = 0
root = [0,"filename"] # (serverID, filename)
fileCount = [] # [(serverID, leafCount, nodeCount),..]

def readMetaData():
	global numServer, root, leafCount, nodeCount
	f = open('metadata','r')
	lines = f.readlines()
	numServer = int(lines[0].strip())
	root = lines[1].strip().split()
	root[0] = int(root[0])
	for i in range(0,numServer):
		fileCount.append(map(int,lines[i+2].strip().split()))
	f.close()

readMetaData()
print fileCount

# read contents from files servermap, metadata, scores.


# TODO Query handler

# TODO New Node Creator




# call stats.py when needed 

# TODO push content to CDN