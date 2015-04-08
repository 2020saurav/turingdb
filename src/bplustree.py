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
			self.ptr.append({'serverID' : 'SXX', 'filename': 'unoccupied'})
		self.parent = {'serverID' : 'SXX', 'filename': 'unoccupied'}
		self.left = {'serverID' : 'SXX', 'filename': 'unoccupied'}
		self.right = {'serverID' : 'SXX', 'filename': 'unoccupied'}
	
	def printToFile(self, filename):
		# to print node content to file.
		with open(filename, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['filename']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['filename'])
			f.write('\n' + self.left['serverID'] + '\t' + self.left['filename'])
			f.write('\n' + self.right['serverID'] + '\t' + self.right['filename'])
			# TODO append garbage

	def readFromFile(self, filename):
		f = open(filename, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'filename': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'filename': sidFile[1]}
		sidFile = lines[4].strip().split('\t')
		self.left = {'serverID' : sidFile[0], 'filename': sidFile[1]}
		sidFile = lines[5].strip().split('\t')
		self.right = {'serverID' : sidFile[0], 'filename': sidFile[1]}
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
			self.ptr.append({'serverID' : 'SXX', 'filename': 'unoccupied'})
		self.parent = {'serverID' : 'SXX', 'filename': 'unoccupied'}
	
	def printToFile(self, filename):
		# to print node content to file.
		with open(filename, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['filename']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['filename'])

	def readFromFile(self, filename):
		f = open(filename, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'filename': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'filename': sidFile[1]}
		f.close()

def isLeaf(s):
	return s[0] == 'L'

def findLeaf(key, filename):
	if isLeaf(filename):
		return (myServerId, filename)
	else:

		n = Node()
		n.readFromFile(filename)
		for i in range(0, n.keyCount+1):
			if i == n.keyCount or key <= n.key[i]:
				pass
		# TODO get the childNode = (serverID, filename) dict from n.ptr[i]
		childNode = { 'serverID' : 'S05', 'filename' : 'F0001'}
		if childNode['serverID'] == myServerId:
			result = findLeaf(key, childNode['filename'])
		else:
			query = 'FINDLEAF$'+str(key)+'$'+childNode['filename']
			result = client.request(childNode['serverID'], query)
		return result


def splitNode(myNode):
	pass
	# get middle key.
	# make call to central server to getNewNode().
	# prepare content to write on this new file
	# make changes to current myNode
	# inform half of the children about change of their parent

	# if current one is a ROOT (of tree) node
	# make appropriate changes. new root setting
	# else inform parent about new sibling

def insertInNode(myNode, key, child):
	pass
	# assert that insertion file is in this server
	# open file, read, find position, insert
	# adjust child pointers, keycount++
	# now if size limits, split

a = Leaf()
# a.printToFile('whatever')
a.readFromFile('whatever')
print a.parent