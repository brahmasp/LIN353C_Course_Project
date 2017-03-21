#!/usr/bin/env python3

import glob
import re

from collections import Counter


# Method to get word to frequency map
def get_word_freq(words):

    word_freq_map = {};

    return Counter(words);


# Method to remove top and bottom metadata info from corpus
def remove_book_metadata(text):
    re_start = re.search(r'\*\*\*\s?START.*\*\*\*', text)
    re_end = re.search(r'\*\*\*\s?END.*\*\*\*', text)
    core_text = text[re_start.span()[1] : re_end.span()[0]-1].strip()
    
    return core_text;


# Filteration method 
# Portable based on filter required

# TEMP: hardcoded to include alphanumeric and apostrophe
def filter(words, filter):

    for index, word in enumerate(words):
        words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# Method that starts the program
def main():

    num_files = 1;

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



        #print(word_freq);
        break;



main();

    
