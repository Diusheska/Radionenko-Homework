# This module 'punctuation' pre-insitialized string which holds all special characters
import string

# I decided to use Counter as I've read it's much more efficient than doing counts with loops
from collections import Counter

f = open("Book.txt")

# read file as string
text = f.read()
# convert everything to lower_case
text = text.lower()
# get rid of all special characters except
for symb in string.punctuation:
    text = text.replace(symb,' ')

# split text into words and count each word occurance
word_count = Counter(text.split())
for word in word_count:
    if word_count[word] > 1: # This is what I understood from lesson, but if we want all words we could simply comment out this line
        print(f"{word} {str(word_count[word])} time(s)")
f.close()
