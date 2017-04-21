#!/usr/bin/env python3

'''
Code below performs TDIDF numerical stats on a given mystery file to identify
and other data sets (that "train" the algorithm 

TFIDF: Measures the importance of a word in a given corpus
'''
from collections import Counter
import glob
import math
import re
import operator

# Method to remove top and bottom metadata info from corpus
def remove_book_metadata(text):
	re_start = re.search(r'\*\*\*\s?START.*\*\*\*', text)
	re_end = re.search(r'\*\*\*\s?END.*\*\*\*', text)
	core_text = text[re_start.span()[1] : re_end.span()[0]-1].strip()

	return core_text;

# TODO
# TEMP: hardcoded to include alphanumeric and apostrophe
def filter_words(words, filter):

	for index, word in enumerate(words):
		words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# Method to get word to frequency map
def get_word_freq(words):
	return dict(Counter(words));


def check_tfidf_closeness(tfidf_map, test_tfidf_map, test_filename):

	# tfidf_map is of form
	"""
	{
		filename1: {
			word1: tfidf score
			word2: tfidf score
		}
		filename1: {
			word1: tfidf score
			word2: tfidf score
		}

	}
	"""

	#test_tfidf_map is of form
	"""	
	{
		test_file: {
			word1: tfidf score
			word2: tfidf score
		}
	}

	"""

	test_tfidf_score = test_tfidf_map[test_filename];

	match_error_map = {};
	for train_data in tfidf_map:

		sq_error = 0;

		for test_word in test_tfidf_score:
			if test_word not in tfidf_map[train_data]:
				sq_error = sq_error + (test_tfidf_score[test_word])**2
			else:
				sq_error = sq_error + (test_tfidf_score[test_word] - tfidf_map[train_data][test_word])**2

		match_error_map[train_data] = sq_error;

	match_error_map_sorted = sorted(match_error_map.items(), key = operator.itemgetter(1))

	for index, filename in enumerate(match_error_map_sorted):
		# f = open(test_filename, 'r', encoding='utf8')
		# auth_name = get_author_name(f.read());
		# print (auth_name + " " + str(filename[1]))
		print("Rank: " + str(index + 1) + " file name: " + filename[0]);


def get_tfidf_map(file_list_contents, word_counts_per_file):

	tfidf_map = {};

	total_docs = len(file_list_contents);

	# For each file
	for filename in file_list_contents:

		# Get word count freq for each file
		word_count_freq = word_counts_per_file[filename]
		tfidf_scores = {};

		# Getting tfidf score for each word in the given document
		# Get count of the given word and check occurence
		# in other docs
		for word in word_count_freq:
			count_per_doc = word_count_freq[word];
			occurence_other_doc = 0;

			# Go through all the word count maps
			# of each file to see if the current word
			# exists in other docs.
			# Value should be minimum always 1
			for other_file in word_counts_per_file:
				if word in word_counts_per_file[other_file]:
					occurence_other_doc += 1;

			tfidf_score = count_per_doc * math.log10(total_docs / occurence_other_doc);
			tfidf_scores[word] = tfidf_score;
		
		tfidf_map[filename] = tfidf_scores;

	# Returning map of file name -> tfidf of every word in the given doc
	return tfidf_map;

def train_data_word_freq():


	file_list_contents = [];

    # Dictionary of filename to word_freq map
	word_counts_per_file = {};

    # Cycle through all the test files
	for filename in glob.glob('books/*.txt'):
		f = open(filename, 'r', encoding='utf8')

		# Read the file
		text = f.read()

		# Extracting core content - removing metadata
		text = remove_book_metadata(text);

		# Vector of all the from a given book
		words = text.split();

		# Filter words to include alphanumeric and apostrophe
		filter_words(words, "");


		# Need to get word-frequency of this text and store it
		# This information is linked to the author who wrote it

		# Store the information and just compare it
		word_freq = get_word_freq(words);

		if filename not in word_counts_per_file:
		    word_counts_per_file[filename] = word_freq;
		else:
		    print("Error: same file name! " + filename)

		if filename not in file_list_contents:
			file_list_contents.append(filename);
		else:
			print("Content of file already recorded");

	
	# At this point
	# Have map from file name to its contents
	# Have map from file name to count of each word in that file

	"""
	iterate through map keys
	
	outer for loop is iterating over files
	inner for loop iterating over all words in the doc
		for a given word in a given doc
		can get the count
		but need to iterate over other maps and see if word
		exists

		then get tfidf for that word and given doc and store it
	"""

	tfidf_map = get_tfidf_map(file_list_contents, word_counts_per_file);

	return tfidf_map;

def detect_author_word_freq(tfidf_map, test_name):

	test_file_list_contents = [];

    # Dictionary of filename to word_freq map
	test_word_counts_per_file = {};

	for test_filename in glob.glob(test_name):    
		f = open(test_filename, 'r', encoding='utf8')

		# Read the file
		test_text = f.read()

		# Extracting core content - removing metadata
		test_text = remove_book_metadata(test_text);

		# Vector of all the from a given book
		test_words = test_text.split();

		# Filter words to include alphanumeric and apostrophe
		filter_words(test_words, "");

		# Need to get word-frequency of this text and store it
		# This information is linked to the author who wrote it

		# Store the information and just compare it
		test_word_freq = get_word_freq(test_words);


		# Need to check similarity of this test item to trained
		# corupus.
		# Traverse through test data and compare frequency for
		# a given word with training data
		# Count the number of times there was a success
		# Success is measured if given the word existed in both dictionaries
		# its difference in count == 0


		if test_filename not in test_word_counts_per_file:
		    test_word_counts_per_file[test_filename] = test_word_freq;
		else:
		    print("Error: same file name! " + test_filename)

		if test_filename not in test_file_list_contents:
			test_file_list_contents.append(test_filename);
		else:
			print("Content of file already recorded");

		# Arguments passed into method will always be size
		# one, list has only one element
		# map has one entry filename -> count, map
		test_tfidf_map = get_tfidf_map(test_file_list_contents, test_word_counts_per_file);

		check_tfidf_closeness(tfidf_map, test_tfidf_map, test_filename);




def main():
	
	# Get tfidf for all words
	# sort list of tfidf stats and their corresponding word

	# a tfidf belongs to a document (not author)
	# 2 stores by same author have two different tfids

	# compute tfidf for the mystery document
	# compare its tfidf with all of the tfidfs avilable and check
	# similarity

	# Another way, compute average of tfidfs from different docs
	# by a COMMON author and then compare it with the tfidf
	# of the new doc


	# After training the data structure should be
	# Map within map
	# {file_name: {word1: tfidf, word2: tfdif score}}

	"""
	tfidf 
	= count(word, in one doc) 
		* log(total docs / num docs it appears in)
	"""

	tfidf_map = train_data_word_freq();

	# Testing all files in the test_data directory
	for test_filename in glob.glob('test_data/*.txt'):
		print(" ");
		print("Currently testing file: " + test_filename); 
		detect_author_word_freq(tfidf_map, test_filename);




main();

