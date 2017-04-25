import nltk
from collections import Counter
import glob
import math
import re
import operator
from nltk.corpus import brown
from nltk.tokenize import RegexpTokenizer
from word_freq_impl import remove_book_metadata, dict_mag, cosine_similarity, cosine_based_closeness

# POS BIGRAMS
def bigram_frequencies(filename):
    f = open(filename, 'r', encoding='utf8')

    # Read the file
    text = f.read()

    # Extracting core content - removing metadata
    text = remove_book_metadata(text);

    # now make the counts relative to the number of bigrams
    pos_relative_freq = relative_pos_bigram_freq(text)

    # store each filename with its relative freqency vector
    if filename not in data_stats:
        data_stats[filename] = pos_relative_freq;
    else:
        print("Error: same file name! " + filename)

    return data_stats
    

# create realtive frequencies for bigram lists 
def relative_bigram_freq(text):
    # tokenize the file and split it into its POS tuples
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)

    # create bigrams
    # get bigrams of the parts of speech
    word_bigrams = set(nltk.bigrams(words))
        
    # get the number of bigrams in the file so you can find RELATIVE freq
    num_bigrams = len(word_bigrams)

    # relative freqency of each bigram 
    word_bigrams = dict(Counter(word_bigrams))
    for bigram in word_bigrams:
        word_bigrams[bigram] /= num_bigrams

        # store each filename with its relative freqency vector
        if filename not in data_stats:
            data_stats[filename] = word_bigrams;
        else:
            print("Error: same file name! " + filename) 

    
    pos_tuples = nltk.pos_tag(text)
        
    # get only the parts of speech
    pos_bigrams = list()    
    for word,pos in pos_tuples:
        pos_bigrams.append(pos)

    

    # get bigrams of the parts of speech
    pos_bigrams = set(nltk.bigrams(pos_bigrams))
    
    # get the number of bigrams in the file so you can find RELATIVE freq
    num_bigrams = len(pos_bigrams)

    # relative freqency of each bigram 
    pos_bigrams = dict(Counter(pos_bigrams))
    for bigram in pos_bigrams:
        pos_bigrams[bigram] /= num_bigrams

    return pos_bigrams


# WORD BIGRAMS
# creates bigrams of words 
def word_bigram_frequencies():

    data_stats = {}

    # go through each file and great a relative frequency dictionary
    # of all of the parts of speech bigrams
    f = open(filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text);
        
        # tokenize the file
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
    
        # create bigrams
        # get bigrams of the parts of speech
        word_bigrams = set(nltk.bigrams(words))
        
        # get the number of bigrams in the file so you can find RELATIVE freq
        num_bigrams = len(word_bigrams)

        # relative freqency of each bigram 
        word_bigrams = dict(Counter(word_bigrams))
        for bigram in word_bigrams:
            word_bigrams[bigram] /= num_bigrams

        # store each filename with its relative freqency vector
        if filename not in data_stats:
            data_stats[filename] = word_bigrams;
        else:
            print("Error: same file name! " + filename) 

    return data_stats
