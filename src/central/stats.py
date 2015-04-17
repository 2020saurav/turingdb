import sys
# To use scores file to make calculations
# data is an array of real numbers representing scaled count of number of times a key has been queried
# Suppose key range is 0.000000000 - 1.000000000 [each key will be unique] 
# Assuming some localization in data, we will pick 1 out of 1000 keys (so as to make this array of size 10**6) as representative.
# This key will get updated when any key in +/-500 gets returned as part of some query
# Point Update and Range Update are needed on this array.
#
# data.append()
maxVal = 1e-9
minVal = 1e9
divisions = 1000000
data = []

def p(key):
	# normalized value for occurence of this key
	index = int(key*divisions)
	if index > divisions:
		index = 0
	return data[index]

def magic1(score, probability):
	# z = (x-0.5)*(y-0.5)
	# We need this function to assign bad node to bad data, and good node to good data
	# (0,0) and (1,1) should have highest score. (1,0) and (0,1) should have least score
	return (score-0.5)*(probability-0.5)

def magic2(score, probability):
	# Add two Gaussians with their means at (0,0) and (1,1) and then trim off exterior parts.
	# May add two additional inverted Gaussians with means at (1,0) and (0,1).
	# This may perform better.
	# Other functions can be (magic1)**n : Try visualizing with 3D plots
	return 1 - abs(score-probability)

def penalize(score, occupancy):
	# add weights to these parameters for proper scaling : try empirically
	return score - occupancy

def mutualScore(score, occupancy, probability):
	mScore = magic2(score, probability)
	mScore = penalize(mScore, occupancy)
	return mScore

def trainModel(queryFile):
	pointData = [0] * (divisions+1)
	rangeData = [0] * (divisions+1)
	f = open(queryFile)
	lines = f.readlines()
	f.close()
	for line in lines:
		line = line.strip().split(' ')

		if line[0] == '0': # INSERT QUERY
			pass

		elif line[0] == '1': # POINT QUERY
			point = int(float(line[1])*divisions)
			pointData[point] += 1

		elif line[0] == '2': # RANGE QUERY
			center = int(float(line[1])*divisions)
			radius = int(float(line[2])*divisions)
			left = max(0, center-radius)
			right = min(divisions, center+radius)
			rangeData[left] += 1
			rangeData[right] -= 1

		elif line[0] == '3': # kNN QUERY
			pass
			# center = int(float(line[1])*divisions)
			# k = int(line[2])
			# # arbitrary 2000. Can be made f(k, total_points)
			# left = max(0, center-2000)
			# right = min(divisions, center+2000)
			# rangeData[left] += 1
			# rangeData[right] -= 1

		elif line[0] == '4': # WINDOW QUERY
			left = int(float(line[1])*divisions)
			right = int(float(line[2])*divisions)
			left = max(0, left)
			right = min(divisions, right)
			rangeData[left] += 1
			rangeData[right] -= 1
			
		else:
			print "Unknown Query"
			sys.exit()
	
	for i in range(1, divisions):
		rangeData[i] += rangeData[i-1]

	for i in range(0, divisions):
		rangeData[i] += pointData[i]

	f = open('train.data', 'w+')
	for i in range(0, divisions):
		f.write(str(rangeData[i])+'\n')
	f.close()

def initialize():
	global data, maxVal, minVal
	f = open('train.data')
	i = 0
	lines = f.readlines()

	data = []
	for line in lines:
		value = int(line.strip())
		data.append(value)
		maxVal = max(maxVal, value)
		minVal = min(minVal, value)

	for i in range(0, divisions):
		# data[i] = data[i]*1.0/maxVal
		data[i] = (data[i]-minVal)*1.0/(maxVal-minVal)


if __name__ == '__main__':
	choice = input('Choice: (1) Train on query: ')
	if choice == 1:
		queryFile = raw_input('Query Filepath: ')
		trainModel(queryFile)
	elif choice == 2:
		initialize()
		print data