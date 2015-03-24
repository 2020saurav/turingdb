# To use scores file to make calculations
data = []
# data is an array of real numbers representing scaled count of number of times a key has been queried
# Suppose key range is 0.000000000 - 1.000000000 [each key will be unique] 
# Assuming some localization in data, we will pick 1 out of 1000 keys (so as to make this array of size 10**6) as representative.
# This key will get updated when any key in +/-500 gets returned as part of some query
# Point Update and Range Update are needed on this array.
#
def p(key):
	global data
	return 1

