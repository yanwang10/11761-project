import sys, os

'''
    script to convert feature into different format
'''


def load_arff(filename):
    at_data = False
    feat = []
    label = []
    with open(filename) as f:
        for line in map(lambda x:x.strip(), f.readlines()):
            if not at_data:
                if line == '@DATA':
                    at_data = True
            else:
                seg = line.split(',')
                label.append(seg[0])
                feat.append(seg[1:])
    assert len(feat) == len(label)
    return feat, label

def to_libsvm(feat, label, outfile):
    with open(outfile, 'w') as f:
        for idx in xrange(len(label)):
            f.write(label[idx])
            for j in xrange(len(feat[idx])):
                f.write(' ' + str(j+1) + ':' + feat[idx][j])
            f.write('\n')

if __name__ == '__main__':
    feat, label = load_arff(sys.argv[1])
    to_libsvm(feat, label, sys.argv[2])