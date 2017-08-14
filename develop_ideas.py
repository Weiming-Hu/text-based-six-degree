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

for url in search('"Breaking Code" WordPress blog', stop=20):
    print(url)

url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

target = 'was'
sentences = re.findall(r"(.*? " + target + r" .*?\.)", soup.get_text())

friends = []
for sentence in sentences:
    neis = find_neighbors_in_sentence(target, sentence)
    friends += neis

# there should be a way to know what sentence the friend is coming from
# a way to trace the searching of friends