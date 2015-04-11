import sys
from avg_sen_len import avg_sen_len
from random_feature import random_feature
from w2v_sim import w2v_sim

def load_text(filename):
	text = list()
	article = list()
	content = open(filename, 'r').readlines()
	for i, line in enumerate(content):
		if line.startswith('~') or i == len(content) - 1:
			if len(article) > 0:
				text.append(article)
			article = list()
		else:
			article.append(line.strip().split(' '))
	return text

'''
	Parameter data should be a list:
	[ feature_tuple_1, feature_tuple_2, ...]
	Each tuple should be : ( attrs, values )
	attrs must contain these two fields: name and type
'''
def arff_dump(filename, data):
	f = open(filename, 'w')

	f.write('@RELATION whatever\n')
	for (attrs, values) in data:
		f.write('@ATTRIBUTE %s %s\n' % (attrs['name'], attrs['type']))
	f.write('@DATA\n')
	# check if all value lists have the same length
	l = None
	for (attrs, values) in data:
		if not l:
			l = len(values)
		else:
			assert l == len(values)

	for i in xrange(l):
		v = []
		for (attrs, values) in data:
			v.append(str(values[i]))
		f.write(','.join(v) + '\n')

	f.close()


if __name__ == '__main__':
	if len(sys.argv) <= 3:
		print 'Usage: %s <text file> <label file> <output file>' % sys.argv[0]
		sys.exit(1)
	text_file = sys.argv[1]
	label_file = sys.argv[2]
	output_file = sys.argv[3]

	text = load_text(text_file)
	labels = [int(line.strip()) for line in open(label_file, 'r')]
	data = [ ( {'name':'label', 'type':'{0, 1}'}, labels ) ]
	assert len(labels) == len(text)


	'''
		Call functions to extract features and add to data.
	'''
	data += avg_sen_len(text)
	data += w2v_sim(text)

	'''
		Output the arff file.
	'''
	arff_dump(output_file, data)
