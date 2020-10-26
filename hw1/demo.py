
from collections import Counter
import string
import re

file = open("shakes.txt", "rt")
text_content = re.sub("[-—/]", " ", file.read())
words_strip_puctuation = [word.strip(string.punctuation).lower() for word in text_content.split()]
words_remove_special_characters = map(lambda x: re.sub("(’|').+$", "", x), words_strip_puctuation)
words_remove_special_characters = map(lambda x: re.sub("[‘’（）()“”！？!?,]", "", x), words_remove_special_characters)
words_remove_special_characters = map(lambda x: re.sub("\.$", "", x), words_remove_special_characters)
words_remove_numbers = filter(lambda x: not re.search( r'\d+', x), words_remove_special_characters)
words_remove_urls = filter(lambda x: not re.search( r'www|http|@', x), words_remove_numbers)

wordcount = Counter(words_remove_urls)
#wordcount.most_common(10)
sorted(wordcount.items())
for item in wordcount.items(): print("{}\t{}".format(*item))
