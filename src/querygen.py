import numpy
import random

mu = 0.5
sigma = 0.2

def f():
	x = normal()
	while x >= 1 or x<0:
		x = normal()
	return x

def normal():
	return abs(numpy.random.normal(mu, sigma))

for i in range(0, 200):
	qtype = random.randint(0,4)
	if qtype == 0:
		print qtype, f(), 'hello'
	elif qtype == 1:
		print qtype, f()
	elif qtype == 2:
		print qtype, f(), f()
	elif qtype == 3:
		print qtype, f(), random.randint(10,20)
	elif qtype == 4:
		left = f()
		right = left + random.random()
		print qtype, left, right

