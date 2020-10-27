from nltk import word_tokenize
from nltk import NaiveBayesClassifier
import argparse,sys
import pandas as pd

def prepare_train_set():
    #df1 = pd.read_csv("sms-spam-collection/training.txt", names=['type','content'],delimiter='\t')
    file = open("sms-spam-collection/training.txt", "rt")
    lines = file.readlines()
    train_set = []
    # Strips the newline character
    for line in lines:
        messages = line.split("\t", 1)
        train_set.append((messages[1], messages[0]))
    return train_set
def train_model(train_set):
    all_words = set(word.lower() for passage in train_set for word in word_tokenize(passage[0].strip()))
    _train_set = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train_set]
    classifier = NaiveBayesClassifier.train(_train_set)
    #classifier.show_most_informative_features()
    return [all_words,classifier]
def evaluate_test_set(model):
    all_words = model[0]
    classifier = model[1]
    file = open("sms-spam-collection/test.txt", "rt")
    lines = file.readlines()
    test_set = []
    count = 0
    for line in lines:
        #print(line.strip())
        features = {word: (word in word_tokenize(line.strip().lower())) for word in all_words}
        result = classifier.classify(features)
        test_set.append((result, line))
        count += 1
        print("Count: ",count, " Done!!")
        if count and not count % 20:
            df = pd.DataFrame(test_set, columns=['result', 'content'])
            df.to_csv ('evaluated_test.txt', index = False, header=False, sep="\t")
            #sys.exit()
    df = pd.DataFrame(test_set, columns=['result', 'content'])
    df.to_csv ('evaluated_test.txt', index = False, header=False, sep="\t")
train_set = prepare_train_set()
model = train_model(train_set)
evaluate_test_set(model)
