#!/usr/bin/env python3

from collections import Counter
import glob
import re

# COMPLETE
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

# TEMP: hardcoded to include alphanumeric and apostrophe
def filter_words(words, filter):

    for index, word in enumerate(words):
        words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# Method to "train" algorithm

def train_data():

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
            print("Error same file name! " + filename)

    return data_stats;


# Method that starts the program
def main():

    # Dictionary of filename to frequencies
    # After training data
    data_stats = train_data();
    test_filename = "Bramah_The_Mirror_of_Kong_Ho";

    for filename in glob.glob('books/' + test_filename + '.txt'):    
        f = open(filename, 'r', encoding='utf8')

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
        # Find the squared error. The author corresponding to
        # least error is the closest match
        # Error is simply squared differences
        # (similar approach used in machine learning models) for
        # cost function

        # Squaring it because adding error. If didnt square possible negative
        # numbers may cancel out positive.
        # Possibly resulting error = 0, when in reality it is not
        
        # Comparing word frequencies of trained data and test

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
        

main();

    
