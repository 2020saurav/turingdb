import socket
import sys
import pprint
import random
import time

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
	for i in range(0, 100):
		insert(random.random(), 'hello world')

	while True:
		choice = input('CHOICE (INSERT:0, POINTQUERY:1, RANGEQUERY: 2, KNNQUERY: 3, WINDOWQUERY:4) :')
		
		if choice == 0:
			key = input('KEY: ')
			value = raw_input('VALUE: ')
			response = insert(key, value)
			print response

		elif choice == 1:
			left = input('KEY: ')
			right = left + eps
			response = window1(left, right)
			print response

		elif choice == 2:
			center = input('CENTER: ')
			radius = input('RADIUS: ')
			left = center - radius
			right = center + radius
			response = window1(left, right)
			print response

		elif choice == 3:
			print 'Contact proneet11@gmail.com'

		elif choice == 4:
			left = input('LEFT KEY: ')
			right = input('RIGHT KEY: ')
			response = window1(left, right)
			print response
		
		else:
			break