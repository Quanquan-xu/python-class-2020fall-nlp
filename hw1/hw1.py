from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.util import ngrams
from collections import Counter
import re
import random
import copy
import functools
import operator
import argparse

#nltk.download('punkt')
def read_text():
    file = open("shakes.txt", "rt")
    text = file.read()
    text = re.sub(r'^\[_?.+_?\]$', '', text)
    #text = "The Apache HTTP Server, colloquially called Apache, is a Web server application notable for playing a key role in the initial growth of the World Wide Web. Originally based on the NCSA HTTPd server, development of Apache began in early 1995 after work on the NCSA code stalled. Apache quickly overtook NCSA HTTPd as the dominant HTTP server, and has remained the most popular HTTP server in use since April 1996."
    #text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text
def pre_process(text):
    #Tokenization
    token = word_tokenize(text)
    # Normalizstion
    ##  Convert to lowercases
    token = map(lambda x: x.lower(), token)

    ## remove number order
    token = filter(lambda x: not re.search( r'\d+', x), token)
    ## remove urls
    token = filter(lambda x: not re.search( r'www|http', x), token)

    # Stemming
    #ps = PorterStemmer()
    #token = map(lambda x: ps.stem(x), token)
    return token

def unigramModel(input_word):
    text = read_text()
    # Replace all none alphanumeric characters with spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    token = pre_process(text)
    unigrams = ngrams(token,1)
    wordcount = Counter(unigrams).most_common()
    wordcount = {k[0]: v for k, v in wordcount}
    count_order = {}
    for item in wordcount:
        count = wordcount[item]
        if count_order.get(count):
            count_order[count].append(item)
        else:
            count_order[count] = [item]
    i = 0
    word_sequences = input_word + " "
    i += 1
    while (i <= 100):
        count_index = random.choice(list(count_order.keys()))
        random_word = random.choice(count_order.get(count_index))
        word_sequences = word_sequences + random_word + " "
        i += 1
    print(word_sequences)

def biggramModel(input_word):
    text = read_text()
    token = pre_process(text)
    unique_token = list(set(copy.deepcopy(token)))
    bigrams = ngrams(token,2)
    generate_sentence(input_word,bigrams,unique_token,5)
def trigramModel(input_word):
    text = read_text()
    token = pre_process(text)
    unique_token = list(set(copy.deepcopy(token)))
    trigrams = ngrams(token,3)
    generate_sentence(input_word,trigrams,unique_token,2)
def generate_sentence(input_word,ngrams,unique_token,scope=1):
    wordcount = Counter(ngrams).most_common()
    words = {}
    for item in wordcount:
        _input = item[0][0:-1]
        _output = item[0][-1]
        count = item[1]
        count_order = words.get(_input)
        if not count_order:
            count_order = {}
        if count_order.get(count):
            count_order[count].append(_output)
        else:
            count_order[count] = [_output]
        words[_input] = count_order
    i = 0
    last_word = input_word[-1];
    word_sequences = " ".join(input_word).capitalize() + " "
    i += 1
    while (i <= 100):
        count_order = words.get(tuple(input_word))
        if count_order:
            #available_words = list(count_order.values())[0]
            available_words = functools.reduce(operator.iconcat, list(count_order.values())[0:scope], [])
            random_word = random.choice(available_words)
        else:
            random_word = random.choice(unique_token)
        if last_word in [".", "?","!"]:
            random_word = random_word.capitalize()
        if random_word in [",",":",";",".", "?","!"]:
            word_sequences = word_sequences[0:-1]
        word_sequences = word_sequences + random_word + " "
        last_word = random_word
        input_word.append(random_word.lower())
        input_word.pop(0)
        i += 1
    print(word_sequences)

parser = argparse.ArgumentParser(description='manual to simple n-grams')
parser.add_argument('--model', type=str, default="")
parser.add_argument('--input', type=str, default="")
args = parser.parse_args()
model = args.model
input_word = args.input
if not model or not input_word:
    print("Please input available paramaters")
else:
    if model == "unigram":
        input_word = input_word.split()[0]
        if not input_word:
            print("Please input one available word")
        unigramModel(input_word)
    elif model == "bigram":
        input_word = input_word.split()[0:1]
        if len(input_word) != 1:
            print("Please input one available word")
        biggramModel(input_word)
    elif model == "trigram":
        input_word = input_word.split()[0:2]
        if len(input_word) != 2:
            print("Please input two words")
        else:
            trigramModel(input_word)
    else:
        print("There are not available N-grams Model")




