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
	del vocab['<UNK>']
	avg_sim = list()
	max_sim = list()
	cont_sim_avg = list()
	cont_sim_var = list()
	top_sim_avg = list()
	bot_sim_avg = list()
	dif_sim = list()
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
			'''
			pair = list()
			for i in xrange(len(sen)):
				for j in xrange(i + 1, len(sen)):
					p = inner_product(vocab[sen[i]], vocab[sen[j]])
					pair.append(p)
			art_max += max(pair)
			art_avg += sum(pair) / len(pair)
			'''
		#max_sim.append(art_max / len(article))
		#avg_sim.append(art_avg / len(article))
		if r % 10 == 0:
			print r
		
		s = average(cont_links)
		cont_sim_avg.append(s)
		top = 5
		if len(cont_links) < top:
			top = len(cont_links)
		cont_links = map(lambda a: (a - s) ** 2, cont_links)
		dif_sim.append(average(cont_links[:top]) - average(cont_links[-top:]))

	'''
	return [({'name':'w2v_avg_sim', 'type':'numeric'}, avg_sim), \
			({'name':'w2v_max_sim', 'type':'numeric'}, max_sim)]
	
	'''
	return [({'name':'w2v_cont_avg', 'type':'numeric'}, cont_sim_avg), \
			#({'name':'w2v_cont_var', 'type':'numeric'}, cont_sim_var), \
			#({'name':'w2v_top_avg', 'type':'numeric'}, top_sim_avg), \
			#({'name':'w2v_bot_avg', 'type':'numeric'}, bot_sim_avg)]
			({'name':'w2v_cont_dif', 'type':'numeric'}, dif_sim)]
