# Markov text generator based on that old CS5 assignment
# https://www.cs.hmc.edu/twiki/bin/view/CS5/MarkovMaterialBlack
#
# Call with no arguments to enter all values individually
#
# Or call with the arg k (the order of the Markov model) to use lease.txt and
# callofcthulhu.txt with a max words of 1000 and an outfile of leaseofcthulhu.txt
#
# File written by Sarah Scheffler
# https://github.com/sarahscheffler/

import sys
import random
import pprint

START_CHAR = '~'
PUNCTUATION = ['.','?','!']
END_PUNCTUATION = PUNCTUATION

def markov_model(text, k):
    """
    Accepts a single (large) string and returns a k-order Markov model based on it
    :param text: a large string to train the Markov model.  If the text has any instance
                 of the string START_CHAR, they will be removed.
    :param k: the order of the Markov model to return
    :return: the Markov model in the form of a Python dictionary.  The keys are k-tuples
             and the values are a list of single values that follow that k-tuple in text.
    """

    if k < 1:
        print "k must be at least 1, and it was ", k
        return None

    # preprocess the string
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('"', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace(START_CHAR, '')

    # initialize model and prepare textlist
    split_text = text.split()
    mmodel = {}
    starting_tuple = (START_CHAR,)*k
    mmodel[starting_tuple] = [] # add (~,~,~) : []

    current_tuple = starting_tuple
    for i in range(len(split_text) - k):
        current_word = split_text[i]

        # if this is the beginning or right after punctuation, add to starting_tuple
        if i==0 or any(split_text[i-1][-1]==x for x in PUNCTUATION):
            mmodel[starting_tuple].append(current_word)

        # if this word has punctuation in it, don't add it to the tuples!
        if any(x in current_word for x in PUNCTUATION):
            current_tuple = starting_tuple
            continue

        # else build new tuple
        current_tuple = current_tuple[1:] + (split_text[i],)

        # if new tuple is not in dict, add it
        if current_tuple not in mmodel:
            mmodel[current_tuple] = []

        # add words
        if (i+1 < len(split_text)):
            mmodel[current_tuple].append(split_text[i+1])

    return mmodel

def back_up_tuple(tup):
    """
    Helper function that 'backs up' a tuple to make the first non-START_CHAR element
    into START_CHAR, e.g. ('~','a','b') -> ('~','~','b')
    :param tup: the tuple to 'back up'
    :return: the backed-up tuple
    """
    length = len(tup)
    starting_tuple = (START_CHAR,)*length

    if tup==starting_tuple:
        return tup
    elif tup[0]==START_CHAR:
        return (START_CHAR,) + back_up_tuple(tup[1:])
    else:
        return (START_CHAR,) + tup[1:]

def gen_from_model(mmodel, numwords):
    """
    Accepts a Markov model generated by markov_model and an integer numwords, the number
    of words fonterprer it to print from that model, then generates the text output
    :param mmodel: a dictionary generated by markov_model
    :param numwords: the number of words to return
    :return: Markov-generated text
    """
    if mmodel is None:
        print "Model was None"
        return None

    k = len(mmodel.keys()[0]) # always at least one key: starting_tuple
    starting_tuple = (START_CHAR,)*k

    return_string = ""

    current_tuple = starting_tuple
    for i in range(numwords):

        # if current_tuple not in dictionary, work backward until we find one
        while current_tuple not in mmodel:
            current_tuple = back_up_tuple(current_tuple)

        current_word = random.choice(mmodel[current_tuple])
        return_string += current_word + " "

        # if this word is punctuation, next tuple becomes starting tuple, else add
        # new word to tuple
        if any(current_word[-1]==x for x in PUNCTUATION):
            current_tuple = starting_tuple
        else:
            current_tuple = current_tuple[1:] + (current_word,)

    return return_string

def main(argv):
    if len(argv) >= 1:
        files = ["lease.txt", "callofcthulhu.txt"]
        k = int(argv[0])
        max_words = 10000
        out_file = "leaseofcthulhu.txt"
    else:
        num_files = int(input("How many training files? "))
        files = []
        for i in range(num_files):
            files.append((raw_input("Enter relative filepath for file "+str(i)+": ")))
        k = int(input("Order of the Markov model? "))
        max_words = int(input("Maximum words? (will clip to end with a sentence): "))
        out_file = raw_input("Output file (if blank, prints to terminal): ")
    text = ""
    for filename in files:
        with open(filename, 'r') as f:
            for line in f:
                text += line
    mmodel = markov_model(text,k)
    #pprint.pprint(mmodel)
    words = gen_from_model(mmodel, max_words)
    words = words.replace('.','.\n') # for ease of reading
    while words[-1][-1] not in END_PUNCTUATION:
        words = words[:-1]
    if out_file.isspace() or out_file is '' or out_file is None:
        print words
    else:
        with open(out_file, 'w') as f:
            f.write(words)
    return

if __name__ == "__main__":
    main(sys.argv[1:])
    
