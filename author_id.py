'''
Main program to run author identification on files with algorithms
-> TFIDF
-> POS bigrams
-> word bigrams
-> word counts

'''
import tfidf
import lilianas_portion
import word_freq_impl

def main():
	print(" ");
	print("Beginning TFIDF");
	tfidf.main();
	print(" ");
	print("Beginning POS Bigram");
	lilianas_portion.main();
	print(" ");
	print("Beginning word frequency");
	word_freq_impl.main();
main();
