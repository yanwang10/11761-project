import random

def random_feature(text):
	feature = list()
	for article in text:
		feature.append(random.random())
	return [ ( {'name':'random_feature', 'type':'numeric'}, feature ) ]
