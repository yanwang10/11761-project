
def avg_sen_len(text):
	feature = list()
	for article in text:
		s = sum([len(sen) for sen in article])
		feature.append(s * 1.0 / len(article))
	return [ ( {'name':'avg_sen_len', 'type':'numeric'}, feature ) ]

