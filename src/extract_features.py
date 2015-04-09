import arff
import sys
from avg_sen_len import avg_sen_len

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

def merge(data, names, feature_dict):
	for feature_name, feature_list in feature_dict.items():
		assert len(data) == len(feature_list)
		for row, value in zip(data, feature_list):
			row.append(value)
		names.append(feature_name)

if __name__ == '__main__':
	if len(sys.argv) <= 3:
		print 'Usage: %s <text file> <label file> <output file>' % sys.argv[0]
		sys.exit(1)
	text_file = sys.argv[1]
	label_file = sys.argv[2]
	output_file = sys.argv[3]

	text = load_text(text_file)
	names = ['Label']
	data = [[line.strip()] for line in open(label_file, 'r')]
	assert len(data) == len(text)


	'''
		Call functions to extract features and add to data.
	'''
	merge(data, names, avg_sen_len(text))


	'''
		Output the arff file.
	'''
	arff.dump(output_file, data, relation = 'whatever', names = names)
