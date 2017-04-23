import nltk
from collections import Counter
import glob
import math
import re
import operator
from nltk.corpus import brown
from nltk.tokenize import RegexpTokenizer




# Method to remove top and bottom metadata info from corpus
def remove_book_metadata(text):
    re_start = re.search(r'\*\*\*\s?START.*\*\*\*', text)
    re_end = re.search(r'\*\*\*\s?END.*\*\*\*', text)
    core_text = text[re_start.span()[1] : re_end.span()[0]-1].strip()
    
    return core_text;

# Filteration method 
# Portable based on filter required
# TEMP: hardcoded to include alphanumeric and apostrophe
def filter_words(words, filter):

    for index, word in enumerate(words):
        words[index] = re.sub(r"[^\w']+", "", word, flags=re.UNICODE);

# get a cleaned up list of all the words in the file 
def split_words(filename):
        f = open(filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text);

        # Vector of all the from a given book
        words = text.split();

        # Filter words to include alphanumeric and apostrophe
        filter_words(words, " ")

        return words

# Magnitude of word counts (i.e. treat the word counts as a vector, and
# get its magnitude)
def dict_mag(d):
    ret = 0

    # Add the squares of each element
    for i in d.values():
        ret += i**2

    return math.sqrt(ret)

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

# attempts to find an author with the same level of lexical diversity
def diversity_analysis(training_book, unknown_book):
    print("")

# sentence length 

# creates bigrams of words 
def word_bigrams_frequencies():

    data_stats = {}

    # go through each file and great a relative frequency dictionary
    # of all of the parts of speech bigrams 
    for filename in glob.glob('books/*.txt'):        
        # tokenize the file and split it into its POS tuples
        word_list = split_words(filename)
    
        # create bigrams
        word_bigrams = list(nltk.bigrams(word_list))

        word_relative_freq = relative_bigram_freq(word_bigrams)

        # store each filename with its relative freqency vector
        if filename not in data_stats:
            data_stats[filename] = word_relative_freq;
        else:
            print("Error: same file name! " + filename) 

    return data_stats

# analyze the relative frequencies of POS bigrams
def pos_bigram_frequencies():

    data_stats = {}
    
    # go through each file and great a relative frequency dictionary
    # of all of the parts of speech bigrams 
    for filename in glob.glob('books/*.txt'):
        
        f = open(filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text);

        # now make the counts relative to the number of bigrams
        pos_relative_freq = relative_bigram_freq(text)

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

    print("Stats for closest match (bigram cosine similarity) (best to worst match): ");
    for index, filename in enumerate(filename_angle_sorted):
        # f = open(test_filename, 'r', encoding='utf8')
        # auth_name = get_author_name(f.read());
        # print (auth_name + " " + str(filename[1]))
        print("Rank: " + str(index + 1) + " (" + str(filename[1]) + " rad), File name: " + filename[0]);

    print(" ")

def detect_author_bigram_freq(data_stats, test_name):
    
    # go through each unknown document and get its relative bigram frequency
    for test_filename in glob.glob(test_name):
        f = open(test_filename, 'r', encoding='utf8')

        # Read the file
        text = f.read()

        # Extracting core content - removing metadata
        text = remove_book_metadata(text);
        
        # get the relative bigram frequency 
        test_bigram_freq = relative_bigram_freq(text)

        # get the cosine angle between
        cosine_based_closeness(data_stats, test_bigram_freq)

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

# Method that starts the program
def main():
    # get this here so you don't have to keep doing it for each book
    # it's super slow and only needs to be calculated once
    data_stats = pos_bigram_frequencies()

    # for each unknown document get the best guess of author based on:
    # 1. it's POS bigrams
    # 2. it's lexical diversity
    for test_filename in glob.glob('test_data/*.txt'):
        print(" ");
        print("Currently testing file: " + test_filename);
        detect_author_bigram_freq(data stats, test_filename)
        detect_author_lexical_diversity(test_filename)

        
main()
    
        

    



    
