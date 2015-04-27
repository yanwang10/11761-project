
w2vfile = '../data/LM-train-50.txt'

#@profile
def inner_product(a, b):
	if len(a) != len(b):
		return 0.0
	s = 0.0
	for ia, ib in zip(a, b):
		s += ia * ib
	return s

#@profile
def w2v_sim(text):
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
			vocab[seg[0]] = [float(seg[j]) for j in xrange(1, dim + 1)]
	print count, '/', len(vocab)
	avg_sim = list()
	max_sim = list()
	for r, article in enumerate(text):
		art_max = 0.0
		art_avg = 0.0
		for sen in article:
			pair = list()
			for i in xrange(len(sen)):
				for j in xrange(i + 1, len(sen)):
					p = inner_product(vocab[sen[i]], vocab[sen[j]])
					pair.append(p)
			art_max += max(pair)
			art_avg += sum(pair) / len(pair)

		max_sim.append(art_max / len(article))
		avg_sim.append(art_avg / len(article))
			
	return [({'name':'w2v_avg_sim', 'type':'numeric'}, avg_sim), \
			({'name':'w2v_max_sim', 'type':'numeric'}, max_sim)]
	