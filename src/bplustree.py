M = 10
myServerId = "S05"
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
		# ptr is now an array of tuple/dict
		for i in range(0,M):
			self.key.append(2.000000)
			self.ptr.append("unoccupied")
			# change this ^ to dictionary
		self.parent = "unoccupied"
		self.left = "unoccupied"
		self.right = "unoccupied"
		# all these ptr to tuple/dict
	
	def printToFile(self, filename):
		# to print node content to file.
		with open(filename, "w+") as f:
			f.write(str(self.keyCount)+"\n")
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]+"\t")
			f.write('\n'+self.parent)
			f.write('\n'+self.left)
			f.write('\n'+self.right)
			# TODO save serverID too!

	def readFromFile(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		self.ptr = (lines[2].strip().split('\t')) # TODO read server ID too
		self.parent = lines[3].strip()
		self.left = lines[4].strip()
		self.right = lines[5].strip()
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
			self.ptr.append("unoccupied") # server ID?
		# internal nodes have one more child ptr:
		self.ptr.append("unoccupied")
		self.parent = "unoccupied"
	
	def printToFile(self, filename):
		# to print node content to file.
		with open(filename, "w+") as f:
			f.write(str(self.keyCount)+"\n")
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]+"\t") # Server ID
			f.write('\n'+self.parent)

	def readFromFile(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		self.ptr = (lines[2].strip().split('\t')) # Server ID
		self.parent = lines[3].strip()
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
		childNode = { "serverID" : "S05", "filename" : "F0001"}
		if childNode['serverID'] == myServerId:
			result = findLeaf(key, childNode['filename'])
		else:
			query = "FINDLEAF$"+str(key)+"$"+childNode['filename']
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

