
import os, sys, re, time
from pattern.en import tag

def extract_pos_feat(text):
	pass
	
def explore_pos_feat(text):
	start = time.time()
	for article in text:
		for sent in article:
			tags = tag(sent)
			print tags
	print 'total:', (time.time()-start)




def load_text(filename):
	text = []
	article = []
	content = open(filename, 'r').readlines()
	for i, line in enumerate(content):
		if line.startswith('~') or i == len(content) - 1:
			if len(article) > 0:
				text.append(article)
			article = []
		else:
			# store the whole sentence here
			sent = re.sub('<s>', '', line)
			sent = re.sub('</s>', '', sent).strip()
			article.append(sent)
	return text


if __name__ == '__main__':
	text_file = sys.argv[1]
	text = load_text(text_file)

	explore_pos_feat(text)

# def inner_product(a, b):
# 	if len(a) != len(b):
# 		return 0.0
# 	s = 0.0
# 	for ia, ib in zip(a, b):
# 		s += ia * ib
# 	return s




# def w2v_sim(text):
# 	vocab = dict()
# 	for article in text:
# 		for sentence in article:
# 			for token in sentence:
# 				vocab[token] = list()
# 	f = open(w2vfile, 'r')
# 	line = f.readline()
# 	pair = line.strip().split(' ')
# 	size = int(pair[0])
# 	dim = int(pair[1])
# 	count = 0
# 	for i in xrange(size):
# 		line = f.readline()
# 		seg = line.strip().split(' ')
# 		if seg[0] in vocab:
# 			count += 1
# 			vocab[seg[0]] = [float(seg[j]) for j in xrange(1, dim + 1)]
# 	print count, '/', len(vocab)
# 	avg_sim = list()
# 	max_sim = list()
# 	for r, article in enumerate(text):
# 		art_max = 0.0
# 		art_avg = 0.0
# 		for sen in article:
# 			pair = list()
# 			for i in xrange(len(sen)):
# 				for j in xrange(i + 1, len(sen)):
# 					p = inner_product(vocab[sen[i]], vocab[sen[j]])
# 					pair.append(p)
# 			art_max += max(pair)
# 			art_avg += sum(pair) / len(pair)

# 		max_sim.append(art_max / len(article))
# 		avg_sim.append(art_avg / len(article))
# 		print r
# 	return [({'name':'w2v_avg_sim', 'type':'numeric'}, avg_sim), \
# 			({'name':'w2v_max_sim', 'type':'numeric'}, max_sim)]


	