# this script will implement and test some ideas for how to carry out the research

# use google search interface package
#
# this is referenced from
# https://breakingcode.wordpress.com/2010/06/29/google-search-python/
#
# package document can be found at
# http://pythonhosted.org/google/
#
# package repository can be found at
# https://pypi.python.org/pypi/google
#
from google import search

# parse html
from bs4 import BeautifulSoup
from urllib import urlopen

# find sentences from texts
import re

# customized function
from find_neighbors_in_sentence import find_neighbors_in_sentence


target = 'biology'
friends = []

for url in search(target, start=1, stop=2, num=3):
    print("Processing url %s" % url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    print("Parsing html")
    sentences = re.findall(r"(.*? " + target + r" .*?\.)", soup.get_text())

    for sentence in sentences:
        neis = find_neighbors_in_sentence(target, sentence)
        if len(neis) > 0:
            print("-- Found friends %s in %s" % (str(neis), sentence))
            friends += neis

# remove duplicates in the list
friends = list(set(friends))

# there should be a way to know what sentence the friend is coming from
# a way to trace the searching of friends