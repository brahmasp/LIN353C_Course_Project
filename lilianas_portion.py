#!/usr/bin/env python3

import nltk
from collections import Counter
import glob
import math
import re
import operator
from nltk.corpus import brown
from nltk.tokenize import RegexpTokenizer
from word_freq_impl import remove_book_metadata, dict_mag, cosine_similarity, cosine_based_closeness
from gen_pos import load_pos

# lexical diversity is a measure of how many different words are in the text
def lexical_diversity(text):

    # tokenize the file and split it into its POS tuples
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)


    # get a count of how many unique words there are
    # divide this number by the total number of words to get the
    # percentage of unique words compared to the entire document
    relative_unique_words = len(set(words)) / len(words)

    return relative_unique_words

# creates bigrams of words
def word_bigram_frequencies():

    data_stats = {}

    # go through each file and great a relative frequency dictionary
    # of all of the parts of speech bigrams
    for filename in glob.glob('books/*.txt'):
        pos_tuples = load_pos(filename, is_txt=True)

        # create bigrams
        # get bigrams of the parts of speech
        word_bigram_freq = word_bigram_cnt(pos_tuples)

        # store each filename with its relative freqency vector
        if filename not in data_stats:
            data_stats[filename] = word_bigram_freq
        else:
            print("Error: same file name! " + filename)

    return data_stats


# analyze the relative frequencies of POS bigrams
def pos_bigram_frequencies():

    data_stats = {}

    # go through each file and great a relative frequency dictionary
    # of all of the parts of speech bigrams
    for filename in glob.glob('books/*.txt'):
        pos_tuples = load_pos(filename, is_txt=True)

        # now make the counts relative to the number of bigrams
        pos_bigram_freq = pos_bigram_cnt(pos_tuples)

        # store each filename with its relative freqency vector
        if filename not in data_stats:
            data_stats[filename] = pos_bigram_freq;
        else:
            print("Error: same file name! " + filename)

    return data_stats


def pos_bigram_cnt(pos_tuples):
    pos_list = map(lambda x: x[1], pos_tuples)
    pos_bigrams = nltk.bigrams(pos_list)

    return dict(Counter(pos_bigrams))

def word_bigram_cnt(pos_tuples):
    word_list = map(lambda x: x[0], pos_tuples)
    word_bigrams = nltk.bigrams(word_list)

    return dict(Counter(word_bigrams))

def detect_author_bigram_freq(word_data_stats, pos_data_stats, test_name):

    # go through each unknown document and get its relative bigram frequency
    for test_filename in glob.glob(test_name):
        pos_tuples = load_pos(test_filename, is_txt=True)

        words = map(lambda x: x[0], pos_tuples) # get rid of the POS, only keep words

        # pos_bigram_freq = relative_pos_bigram_freq(pos_tuples)
        pos_bigram_freq = pos_bigram_cnt(pos_tuples)

        # create bigrams
        word_bigram_freq = word_bigram_cnt(pos_tuples)

        print("Estimate based on POS bigrams")
        # get the cosine angle between POS bigrams and the training data
        cosine_based_closeness(pos_data_stats, pos_bigram_freq)
        print(" ")
        print("Estimate based on word bigrams")
        # get the cosine angle between word bigrams and the training data
        cosine_based_closeness(word_data_stats, word_bigram_freq)


# try to guess author based on lexical diversity
def detect_author_lexical_diversity(unknown_book):

        f = open(unknown_book, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text)

        # get the relative lexical diversity of the text
        diversity = lexical_diversity(text)

        # figure out which text most closely matches based on lexical diversity
        lexical_based_closeness(diversity)


def lexical_based_closeness(unknown_book):
    data_stats = {}

    # go through each book in the training set and get its lexical diversity
    for filename in glob.glob('books/*.txt'):
        f = open(filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text)

        # get the relative lexical diversity of the text
        diversity = lexical_diversity(text)

        # squared error between this book's lexical diversity and that of
        # the unknown book
        error = (diversity - unknown_book)**2

        # put the file in the data set with its lexical diversity error
        # from the unknown book's diversity
        if filename not in data_stats:
            data_stats[filename] = error;
        else:
            print("Error: same file name! " + filename)

    # sort the books based from least to greatest error
    error_sorted = sorted(data_stats.items(), key = operator.itemgetter(1))

    # get the best estimate of what book this might be based on
    # which author in the training data had the most similar
    # lexical diversity
    print("Stats for closest match (lexical diversity) (best to worst match): ");
    for index, filename in enumerate(error_sorted):
        print("Rank: " + str(index + 1) + ", File name: " + filename[0]);

def main():
    # get this here so you don't have to keep doing it for each book
    # it's super slow and only needs to be calculated once
    pos_bigrams = pos_bigram_frequencies()
    word_bigrams = word_bigram_frequencies()

    # for each unknown document get the best guess of author based on:
    # 1. it's POS bigrams
    # 2. it's lexical diversity
    for test_filename in glob.glob('test_data/*.txt'):
        print(" ");
        print("Currently testing file: " + test_filename);
        detect_author_bigram_freq(word_bigrams, pos_bigrams, test_filename)
        # detect_author_lexical_diversity(test_filename)

        
# Method that starts the program
if __name__ == "__main__":
    main();
