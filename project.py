#!/usr/bin/env python3

import glob
import re

from collections import Counter



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

    word_freq_map = {};

    return Counter(words);

# Filteration method 
# Portable based on filter required

# TEMP: hardcoded to include alphanumeric and apostrophe
def filter(words, filter):

    for index, word in enumerate(words):
        words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# Method to "train" algorithm

def train_data():

    num_files = 1;

    # Dictionary of filename to word_freq map
    data_stats = {};

    # Cycle through all the test files
    for filename in glob.glob('books/*.txt'):
        f = open(filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text);

        # File count
        num_files = num_files + 1;

        # Vector of all the from a given book
        words = text.split();

        # Filter words to include alphanumeric and apostrophe
        filter(words, "");

        # Need to get word-frequency of this text and store it
        # This information is linked to the author who wrote it

        # Store the information and just compare it
        word_freq = get_word_freq(words);

        if filename not in data_stats:
            data_stats[filename] = word_freq;
        else:
            print("Error same file name!")

    return data_stats;


# Method that starts the program
def main():

    data_stats = train_data();
    

main();

    
