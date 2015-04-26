from extract_features import arff_dump
import sys

def arff_load(filename):
	content = open(filename, 'r').readlines()
	feature_list = []
	for line in content:
		if len(line) < 2:
			continue
		if line.startswith('@'):
			line = line.lower()
			seg = line.strip().split(' ')
			if line.startswith('@attribute'):
				feature_list.append([seg[1], ' '.join(seg[2:]), []])
				print feature_list[-1]
		else:
			seg = line.strip().split(',')
			assert len(seg) == len(feature_list)
			for i, s in enumerate(seg):
				if 'numeric' == feature_list[i][1]:
					feature_list[i][2].append(float(s))
				else:
					feature_list[i][2].append(s)
			continue
	fd = dict()
	for f in feature_list:
		fd[f[0]] = ({'name':f[0], 'type':f[1]}, f[2])
	return fd

def merge_dict(dst, src):
	for key, value in src.items():
		if not key in dst:
			dst[key] = value
	return dst

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: <dst> <src1> <src2>...'
		exit(0)
	dst = sys.argv[1]
	data = {}
	real_data = []
	for i in xrange(2, len(sys.argv)):
		data = merge_dict(data, arff_load(sys.argv[i]))
	LABEL = 'label'
	if LABEL in data:
	 	real_data.append(data[LABEL])
	for key, value in data.items():
		if key != LABEL:
			real_data.append(value)
	arff_dump(dst, real_data)

