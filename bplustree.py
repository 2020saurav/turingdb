M = 10
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
			self.ptr.append("unoccupied")
		self.parent = "unoccupied"
		self.left = "unoccupied"
		self.right = "unoccupied"
	
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

	def readFromFile(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		self.ptr = (lines[2].strip().split('\t'))
		self.parent = lines[3].strip()
		self.left = lines[4].strip()
		self.right = lines[5].strip()

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
			self.ptr.append("unoccupied")
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
				f.write(self.ptr[i]+"\t")
			f.write('\n'+self.parent)

	def readFromFile(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		self.ptr = (lines[2].strip().split('\t'))
		self.parent = lines[3].strip()
