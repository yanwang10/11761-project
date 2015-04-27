#! /usr/bin/env python

import os, sys
from math import log
import extract_features as ef

TEMP_TEST_FILE = 'temp_test.dat'
PARAM_FILE = 'param.json'
TEMP_FEAT_FILE = 'temp_feat'
CLASSIFIER_PATH = './liblinear/predict'
CLASSIFIER_MODEL = './models/model.11761'
TEMP_OUTPUT_FILE = 'temp_predict'

self_eval = True

'''
    save stdin to temp file
'''
lines = sys.stdin.readlines()
with open(TEMP_TEST_FILE, 'w') as f:
    for line in lines:
        f.write(line)

'''
    feature extraction and classification
'''
ef.get_test_feature(TEMP_TEST_FILE, PARAM_FILE, TEMP_FEAT_FILE)

# run the classifier
# predict [options] test_file model_file output_file
cmd = '{0} -b 1 -q {1} {2} {3}'.format(CLASSIFIER_PATH, TEMP_FEAT_FILE, \
    CLASSIFIER_MODEL, TEMP_OUTPUT_FILE) 
os.system(cmd)

# print the result
with open(TEMP_OUTPUT_FILE) as f:
    for line in map(lambda x:x.strip(), f.readlines()):
        if line.startswith('label'):
            continue
        seg = line.split(' ')
        print seg[1], seg[2], seg[0]

'''
    self evaluation
'''
if self_eval:
    pred = []
    with open(TEMP_OUTPUT_FILE) as f:
        for seg in map(lambda x:x.strip().split(' '), f.readlines()):
            if seg[0].startswith('label'):
                continue
            pred.append((int(seg[0]), float(seg[1]), float(seg[2])))
    real = []
    with open('./data/developmentSetLabels.dat') as f:
        for line in map(lambda x: x.strip(), f.readlines()):
            real.append(int(line))
    assert len(pred) == len(real)
    size = len(pred)
    
    correctness = 0
    T_to_F = 0
    F_to_T = 0
    log_posterior = 0.0
    for idx in xrange(size):
        if real[idx] == pred[idx][0]:
            correctness += 1
        else:
            if real[idx] == 0:
                F_to_T += 1
            else:
                T_to_F += 1
        if pred[idx][real[idx]+1] < 0.001:
            log_posterior += log(0.001)
        else:
            log_posterior += log(pred[idx][real[idx]+1])
    print 'Hard correctness:', float(correctness) / size
    print 'Ture to False:', float(T_to_F) / size
    print 'False to Ture:', float(F_to_T) / size
    print 'Soft avg. log posetrior:', log_posterior / size
    
'''
    clean up
'''
os.system('rm temp*')






