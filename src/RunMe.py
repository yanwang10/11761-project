#! /usr/bin/env python

import os, sys
import extract_features as ef

TEMP_TEST_FILE = 'temp_test.dat'
PARAM_FILE = 'param.json'
TEMP_FEAT_FILE = 'temp_feat'
CLASSIFIER_PATH = './liblinear/predict'
CLASSIFIER_MODEL = 'model.11761'
TEMP_OUTPUT_FILE = 'temp_predict'

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
cmd = '{0} -b 1 {1} {2} {3}'.format(CLASSIFIER_PATH, CLASSIFIER_MODEL, TEMP_OUTPUT_FILE) 
os.system(cmd)

# print the result
with open(TEMP_OUTPUT_FILE) as f:
    for line in f.readlines():
        print line

'''
    clean up
'''
os.system('rm ' + TEMP_TEST_FILE)
os.system('rm ' + TEMP_FEAT_FILE)
os.system('rm ' + TEMP_OUTPUT_FILE)
