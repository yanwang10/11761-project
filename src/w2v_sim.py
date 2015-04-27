import numpy as np
from pattern.en import tag
w2vfile = './models/LM-train-50.txt'

#@profile
def inner_product(a, b):
	#return np.sum(a * b)
	return np.dot(a, b)

def average(l):
	return sum(l) / len(l)

accept_set = set(['JJ', 'VB', 'NN', 'RB'])
def accept(w, t):
	return t[:2] in accept_set

oov = set()

#@profile
def w2v_sim(text, pos = None):
	vocab = dict()
	for article in text:
		for sentence in article:
			for token in sentence:
				vocab[token] = list()
	f = open(w2vfile, 'r')
	line = f.readline()
	pair = line.strip().split(' ')
	size = int(pair[0])
	dim = int(pair[1])
	count = 0
	for i in xrange(size):
		line = f.readline()
		seg = line.strip().split(' ')
		if seg[0] in vocab:
			count += 1
			vocab[seg[0]] = np.array([float(seg[j]) for j in xrange(1, dim + 1)])
	if '<UNK>' in vocab:
		del vocab['<UNK>']
	avg_sim = list()
	cont_sim_avg = list()
	for r, article in enumerate(text):
		art_max = 0.0
		art_avg = 0.0
		cont_links = list()
		for sen in article:
			token_tags = tag(' '.join(sen[1:-1]))
			cont_tokens = list()
			for w, t in token_tags:
				if accept(w, t) and w in vocab:
					cont_tokens.append(w)
			for i in xrange(len(cont_tokens)):
				for j in xrange(i + 1, len(cont_tokens)):
					#p = inner_product(vocab[cont_tokens[i]], vocab[cont_tokens[j]])
					p = np.dot(vocab[cont_tokens[i]], vocab[cont_tokens[j]])
					cont_links.append(p)
			
			pair = list()
			for i in xrange(len(sen)):
				if not sen[i] in vocab:
					continue
				for j in xrange(i + 1, len(sen)):
					if not sen[j] in vocab:
						continue
					p = np.dot(vocab[sen[i]], vocab[sen[j]])
					pair.append(p)
			art_max += max(pair)
			art_avg += sum(pair) / len(pair)
			
		avg_sim.append(art_avg / len(article))
		
		s = average(cont_links)
		cont_sim_avg.append(s)

	return [({'name':'w2v_cont_avg', 'type':'numeric'}, cont_sim_avg), \
			({'name':'w2v_avg_sim', 'type':'numeric'}, avg_sim)]
