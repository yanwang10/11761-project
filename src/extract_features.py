import sys, os
import math
import json
from avg_sen_len import avg_sen_len
from w2v_sim import w2v_sim
from ngram import ngram
from arff_to_libsvm import load_arff, to_libsvm
from pos_feat import load_raw_text, extract_pos_feat


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

def standardize(l, s = None, d = None):
    if not s:
        s = sum(l) * 1.0 / len(l)
    if not d:
        d = math.sqrt(sum([(i - s) ** 2 for i in l]) / len(l))

    for i in xrange(len(l)):
        l[i] = (l[i] - s) / d
    return (s, d)

'''
    Parameter data should be a list:
    [ feature_tuple_1, feature_tuple_2, ...]
    Each tuple should be : ( attrs, values )
    attrs must contain these two fields: name and type
'''
def arff_dump(filename, data, param = None):
    f = open(filename, 'w')
    if not param:
        param = {}
    f.write('@RELATION whatever\n')
    for (attrs, values) in data:
        if attrs['name'] != 'label' and attrs['type'] == 'numeric':
            if attrs['name'] in param:
                s = param.get(attrs['name'])[0]
                d = param.get(attrs['name'])[1]
                standardize(values, s, d)
            else:
                (s, d) = standardize(values)
                param[attrs['name']] = (s, d)
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
    return param


'''
    IMPORTANT: function called by RunMe
'''
def get_test_feature(text_file, standardize_file, output_file):

    param = json.loads(open(standardize_file, 'r').read())
    text = load_text(text_file)

    labels = [0] * len(text)
    feat = [ ( {'name':'label', 'type':'{0, 1}'}, labels ) ]
    '''
        Call functions to extract features and add to data.
    '''
    feat += avg_sen_len(text)
    feat += w2v_sim(text)
    feat += ngram(text, './models/3.binlm', 'tri')
    feat += ngram(text, './models/4.binlm', 'quad')

    text = load_raw_text(text_file)
    pos_feat = extract_pos_feat(text)
    with open('temp_pos', 'w') as f:
        for line in pos_feat:
            f.write(line)
    pos_labels = load_text('temp_pos')
    feat += ngram(pos_labels, './models/pos3.binlm', 'pos-tri')
    feat += ngram(pos_labels, './models/pos4.binlm', 'pos-quad')

    '''
        Output the libsvm file.
    '''
    arff_dump('temp_feat.arff', feat, param=param)
    data, label = load_arff('temp_feat.arff')
    to_libsvm(data, label, output_file)



if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print 'Usage: %s <text file> <label file> <output file> [standardize file]' % sys.argv[0]
        sys.exit(1)
    text_file = sys.argv[1]
    label_file = sys.argv[2]
    output_file = sys.argv[3]
    pos_file = text_file.split(r'/')[-1].replace('dat', 'pos')
    pos_file = './data/' + pos_file
    param = None
    if len(sys.argv) > 4:
        standardize_file = sys.argv[4]
        param = json.loads(open(standardize_file, 'r').read())

    text = load_text(text_file)
    labels = [int(line.strip()) for line in open(label_file, 'r')]
    data = [ ( {'name':'label', 'type':'{0, 1}'}, labels ) ]
    assert len(labels) == len(text)

    '''
        Call functions to extract features and add to data.
    '''
    data += avg_sen_len(text)
    data += w2v_sim(text)
    data += ngram(text, './models/3.binlm', 'tri')
    data += ngram(text, './models/4.binlm', 'quad')

    #print pos_file
    #pos_labels = load_text(pos_file)
    #data += ngram(pos_labels, './models/pos3.binlm', 'pos-tri')
    #data += ngram(pos_labels, './models/pos4.binlm', 'pos-quad')

    '''
        Output the arff file.
    '''
    param = arff_dump(output_file, data, param=param)

    if len(sys.argv) <= 4:
        f = open('param.json', 'w')
        f.write(json.dumps(param, indent = 2))
        f.close()

