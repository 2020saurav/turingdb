M = 10
myServerId = 'S05'
class Leaf(object):
	'''
	Leaf nodes for the bplus tree.
	One dimensional keys, their count, corresponding object pointers are stored
	Parent, left sibling, right sibling also stored for efficiency
	'''
	def __init__(self):
		self.keyCount = 0
		self.key = []
		self.ptr = []
		for i in range(0,M):
			self.key.append(2.000000)
			self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'})
		self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.left = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.right = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
	
	def printToFile(self, fileName):
		# to print node content to file.
		with open(fileName, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['fileName']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['fileName'])
			f.write('\n' + self.left['serverID'] + '\t' + self.left['fileName'])
			f.write('\n' + self.right['serverID'] + '\t' + self.right['fileName'])
			# TODO append garbage

	def readFromFile(self, fileName):
		f = open(fileName, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'fileName': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[4].strip().split('\t')
		self.left = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[5].strip().split('\t')
		self.right = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		f.close()

class Node(object):
	'''
	Internal nodes for the bplus tree.
	One dimensional keys, their count, corresponding child pointers are stored
	Parent also stored for efficiency
	'''
	def __init__(self):
		self.keyCount = 0
		self.key = []
		self.ptr = []
		for i in range(0,M):
			self.key.append(2.000000)
			self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'})
		self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'}) # M + 1 pointers
		self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
	
	def printToFile(self, fileName):
		# to print node content to file.
		with open(fileName, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['fileName']+'\t')
			
			f.write(self.ptr[i]['serverID']+'\t') # M+1 pointers
			f.write(self.ptr[i]['fileName']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['fileName'])

	def readFromFile(self, fileName):
		f = open(fileName, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'fileName': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		f.close()

def isLeaf(s):
	return s[0] == 'L'

def stringify(a, b):
	return a + "$" + b

def stringifyLeaf(leaf):
	'''
	Takes a leaf object and convert its contents into string with $ as separator.
	This will make it easy and uniform way transfer data over network.
	'''
	string = str(leaf.keyCount)
	for i in range(0, M):
		string = string + "$" + str(leaf.key[i])
	for i in range(0, M):
		string = string + "$" + leaf.ptr[i]['serverID'] + "$" + leaf.ptr[i]['fileName']
	string = string + "$" + leaf.parent['serverID'] + "$" + leaf.parent['fileName']
	string = string + "$" + leaf.left['serverID'] + "$" + leaf.left['fileName']
	string = string + "$" + leaf.right['serverID'] + "$" + leaf.right['fileName']
	return string

def stringifyNode(node):
	'''
	Takes a node object and converts its content into string with $ as separator.
	This will make it easy and uniform way transfer data over network.
	'''
	string = str(node.keyCount)
	for i in range(0, M):
		string = string + "$" + str(node.key[i])
	for i in range(0, M+1):
		string = string + "$" + node.ptr[i]['serverID'] + "$" + node.ptr[i]['fileName']
	string = string + "$" + node.parent['serverID'] + "$" + node.parent['fileName']
	return string

def findLeaf(key, fileName):
	'''
	Returns the leaf file corresponding to the key.
	'''
	if isLeaf(fileName):
		response = myServerId + "$" + fileName
		return response
	else:
		n = Node()
		n.readFromFile(fileName)
		for i in range(0, n.keyCount+1):
			if i == n.keyCount or key <= n.key[i]:
				childNode = n.ptr[i]
				break
		# childNode = { 'serverID' : 'S05', 'fileName' : 'F0001'}
		if childNode['serverID'] == myServerId:
			result = findLeaf(key, childNode['fileName']) # local call
		else:
			query = 'FINDLEAF$'+str(key)+'$'+childNode['fileName']
			result = client.request(childNode['serverID'], query) # network call
		return result


def splitNode(fileName):
	'''
	Assumes leaf has M keys, and need to split.
	Find best server for the sibling leaf and pass half data to the sibling.
	Correct left right pointers correspondingly
	Handle case when this leaf is root
	Inform parent about this change
	Inform children about change
	'''
	n = Node()
	sib = Node()
	nextNode = Node()

	n.readFromFile(fileName)
	midKey = n.key[M/2]

	query = "NEWNODE$" + str(midKey)
	response = client.request(centralServerID, query)
	response = response.split('$')
	# make network call to central server to get best server for this new file using key as a guide
	
	sibling = dict()
	sibling['serverID'] = response[0]
	sibling['fileName'] = response[1]

	# fill details in sibling object and then we make a network call to destination server with stringified leaf
	n.keyCount = M/2
	sib.keyCount = M - M/2 - 1
	for i in range(0, sib.keyCount):
		sib.key[i] = n.key[i + M/2 + 1]
		sib.ptr[i] = n.ptr[i + M/2 + 1]

	# children need to be told about their new parent
	if isLeaf(sib.ptr[0]['fileName']):
		child = Leaf()
	else:
		child = Node()
	for i in range(0, sib.keyCount+1):
		node = sib.ptr[i]
		if node['serverID'] != 'SXX':
			if node['serverID'] == myServerId:
				child.readFromFile(node['fileName'])
				child.parent = sibling
				child.printToFile(node['fileName'])
			else:
				# make network call to this server to update parent of this node
				query = "CHANGEPARENT$" + node['fileName'] + "$" + sibling['serverID'] + "$" + sibling['fileName']
				client.request(node['serverID'], query)

	# If current node is root, handle separately.
	query = "WHOISROOT"
	response = client.request(centralServerID, query)
	response = response.split('$')
	root = dict()
	root['serverID'] = response[0]
	root['fileName'] = response[1]

	if myServerId == root['serverID'] and fileName == root['fileName']: # this is root
		query = "NEWNODE$" + str(midKey)
		response = client.request(centralServerID, query)
		response = response.split('$')
		root['serverID'] = response[0]
		root['fileName'] = response[1]
		# usual B+ Node split in case it is the root
		newRoot = Node()
		newRoot.key[0] = midKey
		newRoot.ptr[0] = {'serverID': myServerId, 'fileName': fileName}
		newRoot.ptr[1] = {'serverID': sibling['serverID'], 'fileName': sibling['fileName']}
		newRoot.keyCount = 1
		# save these info about root node
		# TODO : can save a network call here if same serverID
		query = "SAVENODE$" + root['fileName'] + "$" + stringifyNode(newRoot)
		response = client.request(root['serverID'], query)
		# ask central server to change the root.
		query = "CHANGEROOT$" + root['serverID'] + "$" + root['fileName']
		response = client.request(centralServerID, query)
		n.parent = root
		sib.parent = root
		n.printToFile(fileName)
		# print content to files
		if sibling['serverID'] == myServerId:
			sib.printToFile(sibling['fileName'])
		else:
			query = "SAVENODE$" + sibling['fileName'] + "$" + stringifyLeaf(sib)
			response = client.request(sibling['serverID'], query)
	else:
		# this leaf is not root
		sib.parent = n.parent
		n.printToFile(fileName)
		# print to files
		if sibling['serverID'] == myServerId:
			sib.printToFile(sibling['fileName'])
		else:
			query = "SAVENODE$" + sibling['fileName'] + "$" + stringifyLeaf(sib)
			response = client.request(sibling['serverID'], query)
			# network call to save sibling file in its host data server
			# now insert midKey | pointer in parent
			parent = n.parent
			if parent['serverID'] == myServerId:
				insertInNode(parent['fileName'], midKey, sibling)
			else:
				# make network call here
				query = "INSERTINNODE$" + parent['fileName'] + "$" + str(midKey) + "$" + sibling['serverID'] + "$" + sibling['fileName']
				client.request(parent['serverID'], query)


def insertInNode(fileName, key, ptr):
	'''
	Assertively, this node resides on this data server. 
	Open that and insert key and corresponding object ptr in this file.
	'''
	n = Node()
	n.readFromFile(fileName)
	position = 0
	
	while position < n.keyCount and n.key[position] <= key:
		position += 1
	# appropriate position to insert
	for i in range(n.keyCount, position, -1):
		n.key[i] = n.key[i-1]
		n.ptr[i+1] = n.ptr[i]
	# move one ahead
	n.key[position] = key
	n.ptr[position + 1] = ptr
	n.keyCount += 1
	n.printToFile(leafName)

	if n.keyCount == M:
		splitNode(fileName)
		# split has to be handled by the data server whose file is going to split
	return "SUCCESS"

def insertInLeaf(leafName, key, ptr):
	'''
	Assertively, this leaf resides on this data server. 
	Open that and insert key and corresponding object ptr in this file.
	'''
	n = Leaf()
	n.readFromFile(leafName)
	position = 0
	
	while position < n.keyCount and n.key[position] <= key:
		position += 1
	# appropriate position to insert
	for i in range(n.keyCount, position, -1):
		n.key[i] = n.key[i-1]
		n.ptr[i] = n.ptr[i-1]
	# move one ahead
	n.key[position] = key
	n.ptr[position] = ptr
	n.keyCount += 1
	n.printToFile(leafName)

	if n.keyCount == M:
		splitLeaf(leafName)
		# split has to be handled by the data server whose file is going to split

	return "SUCCESS"

def splitLeaf(fileName):
	'''
	Assumes leaf has M keys, and need to split.
	Find best server for the sibling leaf and pass half data to the sibling.
	Correct left right pointers correspondingly
	Handle case when this leaf is root
	Inform parent about this change
	'''
	n = Leaf()
	sib = Leaf()
	nextLeaf = Leaf()

	n.readFromFile(leafName)
	midKey = n.key[M/2]
	
	query = "NEWLEAF$" + str(midKey)
	response = client.request(centralServerID, query)
	response = response.split('$')
	# make network call to central server to get best server for this new file using key as a guide
	
	sibling = dict()
	sibling['serverID'] = response[0]
	sibling['fileName'] = response[1]

	n.keyCount = M/2
	sib.keyCount = M-M/2
	for i in range(0, sib.keyCount):
		sib.key[i] = n.key[i + M/2]
		sib.ptr[i] = n.ptr[i + M/2]

	# fill details in sibling object and then we make a network call to destination server with stringified leaf
	right = n.right
	
	# correct left pointer of old next sibling to point to current new sibling
	if right['serverID'] != 'SXX':
		sib.right = right
		if right['serverID'] == myServerId:
			nextLeaf.readFromFile(right['fileName'])
			nextLeaf.left = sibling
			nextLeaf.printToFile(right['fileName'])
		else:
			# its left pointer to point to sibling.
			# correct sib.right to point to this
			query = "CHANGELEFTPTR$" + right['fileName'] + "$" + sibling['serverID'] + "$" + sibling['fileName']
			response = client.query(right['serverID'], query)

	n.right = sibling
	sib.left = {'serverID': myServerId, 'fileName': leafName}
	# left/right things done. parent setting done below
	# If current leaf is root, handle separately. Happens in the beginning only once
	query = "WHOISROOT"
	response = client.request(centralServerID, query)
	response = response.split('$')
	root = dict()
	root['serverID'] = response[0]
	root['fileName'] = response[1]

	if myServerId == root['serverID'] and fileName == root['fileName']: # this is root
		query = "NEWNODE$" + str(midKey)
		response = client.request(centralServerID, query)
		response = response.split('$')
		root['serverID'] = response[0]
		root['fileName'] = response[1]
		# usual B+ Leaf split in case it is the root
		newRoot = Node()
		newRoot.key[0] = midKey
		newRoot.ptr[0] = {'serverID': myServerId, 'fileName': fileName}
		newRoot.ptr[1] = {'serverID': sibling['serverID'], 'fileName': sibling['fileName']}
		newRoot.keyCount = 1
		# save these info about root node
		# TODO : can save a network call here if same serverID
		query = "SAVENODE$" + root['fileName'] + "$" + stringifyNode(newRoot)
		response = client.request(root['serverID'], query)
		# ask central server to change the root.
		query = "CHANGEROOT$" + root['serverID'] + "$" + root['fileName']
		response = client.request(centralServerID, query)
		n.parent = root
		sib.parent = root
		n.printToFile(fileName)
		# print content to files
		if sibling['serverID'] == myServerId:
			sib.printToFile(sibling['fileName'])
		else:
			query = "SAVELEAF$" + sibling['fileName'] + "$" + stringifyLeaf(sib)
			response = client.request(sibling['serverID'], query)
	else:
		# this leaf is not root
		sib.parent = n.parent
		n.printToFile(fileName)
		# print to files
		if sibling['serverID'] == myServerId:
			sib.printToFile(sibling['fileName'])
		else:
			query = "SAVELEAF$" + sibling['fileName'] + "$" + stringifyLeaf(sib)
			response = client.request(sibling['serverID'], query)
			# network call to save sibling file in its host data server
			# now insert midKey | pointer in parent
			parent = n.parent
			if parent['serverID'] == myServerId:
				insertInNode(parent['fileName'], midKey, sibling)
			else:
				# make network call here
				query = "INSERTINNODE$" + parent['fileName'] + "$" + str(midKey) + "$" + sibling['serverID'] + "$" + sibling['fileName']
				client.request(parent['serverID'], query)

# a = Leaf()
# a.printToFile('whatever')
# a.readFromFile('whatever')
# print a.parent