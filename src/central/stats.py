import sys
# To use scores file to make calculations
data = []
# data is an array of real numbers representing scaled count of number of times a key has been queried
# Suppose key range is 0.000000000 - 1.000000000 [each key will be unique] 
# Assuming some localization in data, we will pick 1 out of 1000 keys (so as to make this array of size 10**6) as representative.
# This key will get updated when any key in +/-500 gets returned as part of some query
# Point Update and Range Update are needed on this array.
#
# data.append()
maxVal = 1e-9
def p(key):
	global data
	# get corresponding scaled probability for this key
	# keep updating maxVal, and return val/maxVal for normalized [0,1] range output
	return 1/maxVal

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
	return 1

def penalize(score, occupancy):
	# add weights
	return score - occupancy

def mutualScore(score, occupancy, probability):
	mScore = magic1(score, probability)
	mScore = penalize(mScore, occupancy)
	return mScore

def trainModel(queryFile):
	divisions = 1000000
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
			center = int(float(line[1])*divisions)
			k = int(line[2])
			# arbitrary 2000. Can be made f(k, total_points)
			left = max(0, center-2000)
			right = min(divisions, center+2000)
			rangeData[left] += 1
			rangeData[right] -= 1

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




if __name__ == '__main__':
	choice = input('Choice: (1) Train on query: ')
	if choice == 1:
		queryFile = raw_input('Query Filepath: ')
		trainModel(queryFile)