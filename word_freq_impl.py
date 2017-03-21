#!/usr/bin/env python3

from collections import Counter
import glob
import re
import operator

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


# Method to comapre the test data vs trained data to detect best match
def detect_author(data_stats, test_name):

    for test_filename in glob.glob('books/' + test_name + '.txt'):    
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

        
        # Comparing word frequencies of trained data and test
        # Map of filename to error with regard to test and data file
        filename_error_map = {};

        test_file_num_words = len(test_word_freq);
        success = 0;
        # For a given corpus file, 
        # traverse through all words of test file
        for data_filename in data_stats:

            # Initially zero error with respect to test data
            filename_error_map[data_filename] = 0;
            for word in test_word_freq:

                # If the frequency of a given word in test and data file is 0, then success
                if word in data_stats[data_filename] and (data_stats[data_filename][word] - test_word_freq[word]) == 0:
                    success += 1;

            filename_error_map[data_filename] = (success / test_file_num_words) * 100;
            success = 0;

        # After accumulating all the errors.
        # Need to find min error and get corresponding filename
        # This filename is the closest match
        num_training_files = len(data_stats);

        # Returns a tuple of sorted file names based on value (the error)
        filename_error_sorted = sorted(filename_error_map.items(), key = operator.itemgetter(1), reverse = True)

        print("Below are the stats for closest match (best to worst match): ");
        for filename in filename_error_sorted:

            # f = open(test_filename, 'r', encoding='utf8')
            # auth_name = get_author_name(f.read());
            # print (auth_name + " " + str(filename[1]))
            print(filename[0] + " " + str(filename[1]));


# Method that starts the program
def main():

    # Dictionary of filename to frequencies
    # After training data
    data_stats = train_data();

    test_name = "Mrs. Alexander_Kate Vernon Vol2";
    detect_author(data_stats, test_name);

main();

    
