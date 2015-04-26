#! /usr/bin/env python

import os, sys

def main(train):

    # do feature extraction here

    with open(train) as f:
        print f.readlines()



if __name__ == '__main__':
    # save stdin to temp file
    lines = sys.stdin.readlines()
    with open('temp_train', 'w') as f:
        for line in lines:
            f.write(line)

    # feature extraction and classification
    main('temp_train')

    # clean up
    os.system('rm temp_train')

