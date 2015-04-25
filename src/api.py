import socket
import sys
import pprint
import random
import time
import numpy as np

eps = 1e-6

def request(query):
	s = socket.socket()
	server = {'IP': '127.0.0.1', 'port': 2020}
	s.connect((server['IP'], server['port']))
	s.send(str('%05d'%len(query)))
	s.send(query)
	# wait for response
	responseLength = int(s.recv(5))
	response = s.recv(responseLength)
	s.close()
	return response

def insert(key, data):
	query = 'INSERT$' + str(key) + '$' + data
	response = request(query)
	return response

def window1(left, right):
	# includes left, excludes right.
	query = 'WINDOW1$' + str(left) + '$' + str(right)
	response = request(query)
	return response

if __name__=='__main__':

	statsInsertQuery = []
	statsPointQuery = []
	statsRangeQuery = []
	statsKNNQuery = []
	statsWindowQuery = []

	buildTree = True # must start data servers before central server
	runQuery = True
	inputFile = 'small.in'
	queryFile = 'small.qr'
	startTime = time.time()

	if buildTree:
		print 'Tree building started at ', time.time()
		f = open(inputFile)
		lines = f.readlines()
		f.close()
		for line in lines:
			line = line.strip().split(' ')
			insert(float(line[0]), line[1])
		print 'Tree building ended at ', time.time()

	if runQuery:
		print 'Query processing started at ', time.time()
		f = open(queryFile)
		lines = f.readlines()
		f.close()
		for line in lines:
			line = line.strip().split(' ')
			choice = int(line[0])

			if choice == 0:
				start = time.time()
				key = float(line[1])
				value = line[2]
				response = insert(key, value)
				end = time.time()
				statsInsertQuery.append(end-start)
				# print response

			elif choice == 1:
				start = time.time()
				left = float(line[1])
				right = left + eps
				response = window1(left, right)
				end = time.time()
				statsPointQuery.append(end-start)
				# print response

			elif choice == 2:
				start = time.time()
				center = float(line[1])
				radius = float(line[2])
				left = center - radius
				right = center + radius
				response = window1(left, right)
				end = time.time()
				statsRangeQuery.append(end-start)
				# print response

			elif choice == 3:
				pass
				# TODO 

			elif choice == 4:
				start = time.time()
				left = float(line[1])
				right = float(line[2])
				response = window1(left, right)
				end = time.time()
				statsWindowQuery.append(end-start)
				# print response
			else:
				pass

		print 'Query Processing ended at ', time.time()		

	print "\nINSERT QUERY\n------------------"
	print "Maximum: \t", np.amax(statsInsertQuery)
	print "Minimum: \t", np.amin(statsInsertQuery)
	print "Mean: \t\t",  np.mean(statsInsertQuery)
	print "Std Dev: \t", np.std( statsInsertQuery)
	print "\nPOINT QUERY\n------------------"
	print "Maximum: \t", np.amax(statsPointQuery)
	print "Minimum: \t", np.amin(statsPointQuery)
	print "Mean: \t\t",  np.mean(statsPointQuery)
	print "Std Dev: \t", np.std( statsPointQuery)
	print "\nRANGE QUERY\n------------------"
	print "Maximum: \t", np.amax(statsRangeQuery)
	print "Minimum: \t", np.amin(statsRangeQuery)
	print "Mean: \t\t",  np.mean(statsRangeQuery)
	print "Std Dev: \t", np.std( statsRangeQuery)
	# print "\nKNN QUERY\n------------------"
	# print "Maximum: \t", np.amax(statsKNNQuery)
	# print "Minimum: \t", np.amin(statsKNNQuery)
	# print "Mean: \t\t",  np.mean(statsKNNQuery)
	# print "Std Dev: \t", np.std( statsKNNQuery)
	print "\nWINDOW QUERY\n------------------"
	print "Maximum: \t", np.amax(statsWindowQuery)
	print "Minimum: \t", np.amin(statsWindowQuery)
	print "Mean: \t\t",  np.mean(statsWindowQuery)
	print "Std Dev: \t", np.std( statsWindowQuery)

	endTime = time.time()
	print "Total Execution Time: ", endTime - startTime