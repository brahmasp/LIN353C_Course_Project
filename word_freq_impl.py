#!/usr/bin/env python3

from collections import Counter
import glob
import math
import re
import operator

# TODO: COMPLETE
def get_author_name(text):

    re_start = re.search(r'Author:', text)
    return -1;


# Method to remove top and bottom metadata info from corpus
def remove_book_metadata(text):
    re_start = re.search(r'\*\*\*\s?START.*\*\*\*', text)
    re_end = re.search(r'\*\*\*\s?END.*\*\*\*', text)
    core_text = text[re_start.span()[1] : re_end.span()[0]-1].strip()
    
    return core_text;


# Method to get word to frequency map
def get_word_freq(words):
    return dict(Counter(words));

# Filteration method 
# Portable based on filter required

# TODO
# TEMP: hardcoded to include alphanumeric and apostrophe
def filter_words(words, filter):

    for index, word in enumerate(words):
        words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# Magnitude of word counts (i.e. treat the word counts as a vector, and
# get its magnitude)
def dict_mag(d):
    ret = 0

    # Add the squares of each element
    for i in d.values():
        ret += i**2

    return math.sqrt(ret)

# Method to "train" algorithm
# Training is based on check occurences of word in a story
def train_data_word_freq():

    # Dictionary of filename to word_freq map
    data_stats = {};

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

        if filename not in data_stats:
            data_stats[filename] = word_freq;
        else:
            print("Error: same file name! " + filename)

    return data_stats;

# Measuring how many times a word was exactly used. Identical frequencies
# is critical in this. A giving a percentage of success. 
# This method is more discrete in that, we consider it to be a success
# or failure imemdiately based on a certain condition (if the counts are
# exact)
def success_based_closeness(data_stats, test_word_freq):

    DECIMAL_FORMAT = 2;
    # Comparing word frequencies of trained data and test
    # Map of filename to error with regard to test and data file
    filename_success_failure_map = {};

    test_file_num_words = len(test_word_freq);
    success = 0;
    # For a given corpus file, 
    # traverse through all words of test file
    for data_filename in data_stats:

        # Initially zero error with respect to test data
        filename_success_failure_map[data_filename] = 0;
        for word in test_word_freq:

            # If the frequency of a given word in test and data file is 0, then success
            if word in data_stats[data_filename] and (data_stats[data_filename][word] - test_word_freq[word]) == 0:
                success += 1;

        filename_success_failure_map[data_filename] = round((success / test_file_num_words) * 100, DECIMAL_FORMAT);
        success = 0;

    # After accumulating all the errors.
    # Need to find min error and get corresponding filename
    # This filename is the closest match
    num_training_files = len(data_stats);   

    # Returns a tuple of sorted file names based on percentage of closeness
    # In descending order
    filename_success_failure_sorted = sorted(filename_success_failure_map.items(), key = operator.itemgetter(1), reverse = True)

    print("Stats for closest match (success-failure method) (best to worst match): ");
    for filename in filename_success_failure_sorted:

        # f = open(test_filename, 'r', encoding='utf8')
        # auth_name = get_author_name(f.read());
        # print (auth_name + " " + str(filename[1]))
        print("Percentage of closeness: " + str(filename[1]) + "%, File name: " + filename[0]);
    
# Measuring count differences (squared errors) and put them in ascending 
# order. In other words, best to worst match
# This method is less structured and is more flexibile in the sense that we
# consider closeness by just measuring difference rather ruling something 
# out because it was not exact
def error_based_closeness(data_stats, test_word_freq):

    filename_error_map = {};

    # For a given corpus file, 
    # traverse through all words of test file
    for data_filename in data_stats:

        # Initially zero error with respect to test data
        filename_error_map[data_filename] = 0;
        for word in test_word_freq:

            # If word that was in test data is not in corpus the error is
            # (count - 0)^2
            # where 0 is because word didnt exist in given file
            if word not in data_stats[data_filename]:
                filename_error_map[data_filename] += (test_word_freq[word]**2);

            # If word does exist, we want to find the squared difference
            else:
                filename_error_map[data_filename] += ((data_stats[data_filename][word] - test_word_freq[word])**2);


    # After accumulating all the errors.
    # Need to find min error and get corresponding filename
    # This filename is the closest match
    num_training_files = len(data_stats);

    # Returns a tuple of sorted file names based on value (the error)
    filename_error_sorted = sorted(filename_error_map.items(), key = operator.itemgetter(1))

    print("Stats for closest match (squared error) (best to worst match): ");
    for index, filename in enumerate(filename_error_sorted):

        # f = open(test_filename, 'r', encoding='utf8')
        # auth_name = get_author_name(f.read());
        # print (auth_name + " " + str(filename[1]))
        print("Rank: " + str(index + 1) + ", File name: " + filename[0]);



# Take the two word frequencies as vectors. Then, take the angles
# between the two vectors as the closeness. Smaller the angle, closer
# the documents.
def cosine_similarity(d1, d2):
    dot_product = 0
    all_words = set().union(d1.keys(), d2.keys())

    # Calculate the numerator (the dot product)
    for i in all_words:
        # The second argument in `get` is a default value; i.e. if `i`
        # doesn't exist in the dict, then return 0
        dot_product += d1.get(i, 0) * d2.get(i, 0)

    # Calculate magnitudes of the two vectors
    d1_mag = dict_mag(d1)
    d2_mag = dict_mag(d2)

    # Take the inverse cosine based on the dot product formula
    return math.acos(dot_product / (d1_mag * d2_mag))

def cosine_based_closeness(data_stats, test_word_freq):

    filename_angle_map = {}

    # For a given corpus file, 
    # traverse through all words of test file
    for data_filename in data_stats:
        # Compare the angle between the current test file, and
        # the training corpus
        filename_angle_map[data_filename] = cosine_similarity(data_stats[data_filename], test_word_freq)


    # After accumulating all the errors.
    # Need to find min error and get corresponding filename
    # This filename is the closest match
    num_training_files = len(data_stats);

    # Returns a tuple of sorted file names based on value (the error)
    filename_angle_sorted = sorted(filename_angle_map.items(), key = operator.itemgetter(1))

    print("Stats for closest match (cosine similarity) (best to worst match): ");
    for index, filename in enumerate(filename_angle_sorted):
        # f = open(test_filename, 'r', encoding='utf8')
        # auth_name = get_author_name(f.read());
        # print (auth_name + " " + str(filename[1]))
        print("Rank: " + str(index + 1) + " (" + str(filename[1]) + " rad), File name: " + filename[0]);

# Method to comapre the test data vs trained data to detect best match
# Based on how often a author uses a word (by measuring a words occurence)
# We measure the closness the test data frequencies are to each author
# Hence determining the closest match

# Given this one way of looking at frequencies, we have two ways
# of measuring closeness

# 1) Measuring how many times a word was exactly used. Identical frequencies
# is critical in this. A giving a percentage of success. 
# This method is more discrete in that, we consider it to be a success
# or failre immedaitely based on a certain condition (if the counts are
# exact)

# 2) Measuring count differences (squared errors) and put them in ascending 
# order. In other words, best to worst match
# This method is less structured and is more flexibile in the sense that we
# consider closeness by just measuring difference rather ruling something 
# out because it was not exact

# 3) Measuring the angle between the two vectors of word frequencies,
# and sorting the results in order of smallest angle. This should
# account for different document sizes.
def detect_author_word_freq(data_stats, test_name):

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


        ''' First impl based on comments above method '''
        success_based_closeness(data_stats, test_word_freq);

        print(" ");
        ''' Second impl based on comments above method '''
        error_based_closeness(data_stats, test_word_freq);

        print(" ");
        ''' Third impl based on comments above method '''
        cosine_based_closeness(data_stats, test_word_freq)

# Method that starts the program
def main():

    # Dictionary of filename to frequencies
    # After training data
    data_stats = train_data_word_freq();

    # Testing all files in the test_data directory
    for test_filename in glob.glob('test_data/*.txt'):
        print(" ");
        print("Currently testing file: " + test_filename); 
        detect_author_word_freq(data_stats, test_filename);

main();

    
