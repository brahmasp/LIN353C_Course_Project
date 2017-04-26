#!/usr/bin/env python3

import nltk
from collections import Counter
import glob
import math
import re
import operator
import json
import codecs
from nltk.corpus import brown
from nltk.tokenize import RegexpTokenizer
from word_freq_impl import remove_book_metadata, dict_mag, cosine_similarity, cosine_based_closeness

def gen_pos(filename):
    f = open(filename, 'r', encoding='utf8')

    # Read the file
    text = f.read()

    # Extracting core content - removing metadata
    text = remove_book_metadata(text);

    # tokenize the file and split it into its POS tuples
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)

    pos_tuples = nltk.pos_tag(text)

    return pos_tuples

def write_pos(tuples, outfile):
    print("Writing to file",outfile)
    with open(outfile, 'w', encoding='utf8') as f:
        # f.write(json.dumps(tuples))
        json.dump(tuples, f, ensure_ascii=False)

def load_pos(infile, is_txt=True):
    if is_txt:
        infile = re.sub(r'\.txt$',"_pos.json",infile)
    with open(infile, 'r', encoding='utf8') as f:
        l = json.loads(f.read(), encoding='UTF-8')
        return list((x[0],x[1]) for x in l)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Need file to generate with", sys.stderr)

    # print(sys.getsizeof(gen_pos(sys.argv[1])))
    write_pos(gen_pos(sys.argv[1]), re.sub(r'\.txt$',"_pos.json",sys.argv[1]))
