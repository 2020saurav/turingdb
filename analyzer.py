import os
M = 40

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
			self.ptr.append('unoccupied')
		self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.left = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.right = {'serverID' : 'SXX', 'fileName': 'unoccupied'}

	def readFromFile(self, fileName):
		f = open(fileName, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		cdnFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(cdnFiles)):
			self.ptr.append(cdnFiles[i])

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[4].strip().split('\t')
		self.left = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[5].strip().split('\t')
		self.right = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		f.close()


if __name__=='__main__':

	l = Leaf()
	data = []
	for i in range(1, 4):
		directory = os.path.join('s0'+str(i)+'/data')
		for root, dires, files in os.walk(directory):
			for file in files:
				if file[0] =='L':
					l.readFromFile(directory +'/' +file)
					for j in range(0, l.keyCount):
						data.append((l.key[j], i))
	data = sorted(data)
	f = open('dist.data', 'w+')
	for datum in data:
		f.write(str(datum[0]) + ', ' + str(datum[1]) + '\n')
	f.close()