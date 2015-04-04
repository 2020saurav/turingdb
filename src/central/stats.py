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

