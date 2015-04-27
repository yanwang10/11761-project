import os

def ngram(text, binlm, prefix):
	n_ppl = list()
	n_ent = list()
	for i, article in enumerate(text):
		f = open('temp', 'w')
		f.write('\n'.join([' '.join(sen) for sen in article]))
		f.close()
		r = os.popen('echo "perplexity -text temp" | ./evallm -binary %s 2> temp_log' % binlm)
		s = r.read()
		seg = s.split('\n')
		for line in seg:
			if 'Perplexity' in line:
				pair = line.split(', ')
				n_ppl.append(float(pair[0].split('=')[-1].strip()))
				ent = pair[1].split('=')[-1]
				ent = ent.strip().split(' ')[0]
				n_ent.append(float(ent))
				break

	return [({'name':'%s_ppl' % prefix, 'type':'numeric'}, n_ppl), \
			({'name':'%s_ent' % prefix, 'type':'numeric'}, n_ent)]

