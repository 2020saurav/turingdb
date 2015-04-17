import numpy
import random

mu = 0.5
sigma = 0.2

def f():
	return uniform()

def uniform():
	return numpy.random.uniform(0.0, 1.0)

def normal():
	return abs(numpy.random.normal(mu, sigma))

for i in range(0, 2000):
	print f(), 'hello'
