# find_path_server.py
# this module does actually the same thing as the local module
# except this will be deployed online

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from urllib.parse import urlencode
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import urllib
import pdb
import sys
import re


number_of_urls_to_search = 3


class wordNode:
    def __init__(self, word: str, sentence: str, url: str):
        # these attributes are requied
        self._word = word
        self._sentence = sentence
        self._url = url
        self.children = []
        self.parent = None

    def __str__(self):
        return 'class wordNode: {} in url<{}> with id {}'.format(
            self._word,
            self._url,
            self._sentence)

    def get_word(self):
        return self._word

    def get_sentence(self):
        return self._sentence

    def get_url(self):
        return self._url

    def add_child(self, newNode):
        self.children.append(newNode)
        newNode.parent = self


def show_sentences(path):
    for node in path:
        if not node.parent:
            continue
        print(node.get_url())
        print(node.get_sentence())
        print('\n')


def show_path(start, end):
    print('\n--------------------------------------')
    reverse_path = [end]
    parentNode = end.parent
    while parentNode:
        reverse_path.append(parentNode)
        parentNode = parentNode.parent
    print('the connection between ({}) and ({}) is displayed as below:'.format(
        start.get_word() , end.get_word()))
    reverse_path.reverse()
    for node in reverse_path:
        print('({word}) in ({url})'.format(
            word=node.get_word(),
            url=node.get_url()
            ))
    print('intermediates: %d' % (len(reverse_path) - 2))
    print('--------------------------------------\n')
    return reverse_path


def find_neighbours_in_one_sentence(target, sentence, url):
    # sentence and url will be used to initialize the wordNode class
    nei = []
    # some cleaning
    sentence, number = re.subn(re.compile('[ ][ ]+'), ' ', sentence)
    sentence, number = re.subn(re.compile('[ ]$'), '', sentence)
    sentence, number = re.subn(re.compile('^[ ]'), '', sentence)
    words = sentence.split(' ')
    assert '' not in words
    # find the neighbours
    for i in range(0, len(words)):
        if words[i].lower() == target.lower():
            tmp = words[i-1 if i>0 else 0 : i+2]
            tmp.remove(words[i])
            for word in tmp:
                new = wordNode(
                        word=word,
                        sentence=sentence,
                        url=url)
                nei.append(new)
    if nei:
        return nei
    else:
        return None


def find_neighbours_in_url(target, url):
    # first parse the url into sentences
    # then call find_neighbours_in_one_sentence() to find neighbours
    found = []
    nei = []
    try:
        html = urlopen(url, timeout=20)
        bsObj = BeautifulSoup(html, 'html.parser')
    except:
        return None
    p_list = bsObj.findAll('p')
    for item in p_list:
        for raw in item.get_text().split('.'):
            processed, number = re.subn(re.compile('[^a-zA-Z ]'), ' ', raw)
            processed, number = re.subn(re.compile('[ ][ ]+'), ' ', processed)
            tmp, test_number = re.subn(re.compile('[a-zA-Z]'), '+', processed)
            if test_number > 5:
                found = find_neighbours_in_one_sentence(target, processed, url)
                if found:
                    nei.extend(found)
    return nei


def bing_search(start, end):
    # Generator: yield the url for beautifulsoup
    global number_of_urls_to_search
    local_count = number_of_urls_to_search
    driver = webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1-windows/bin/phantomJS')
    driver.get("http://global.bing.com/?FORM=HPCNEN&setmkt=en-us&setlang=en-us")
    try:
        element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "sb_feedback")))
    except:
        raise
    finally:
        searchField = driver.find_element(By.ID, "sb_form_q")
        submitButton = driver.find_element(By.ID, "sb_form_go")
    actions = ActionChains(driver).click(searchField).send_keys(start + " " + end + " " + "text").click(submitButton)
    actions.perform()
    try:
        element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "b_footerRight")))
    except:
        raise
    finally:
        bsObj = BeautifulSoup(driver.page_source, 'html.parser')
    results = bsObj.findAll('li', {'class': 'b_algo'})
    for result in results:
        if not local_count:
            driver.close()
            return
        print(result.a['href'])
        yield result.a['href']
        local_count -= 1
    driver.close()


def wiki_bing_search(word):
    # Generator: return a list of urls every time, and iterate 10 times
    # Usage: for urls in wiki_bing_search(word): ******
    global number_of_urls_to_search
    # the first url is from wiki
    url = 'https://en.wikipedia.org/wiki/%s' % word
    yield url

    # then use bing
    values = {
            'setmkt': 'en-us',
            'setlang': 'en-us',
            'q': word,
            }
    first = 0
    while first <= (number_of_urls_to_search-1):
        data = urlencode(values)
        url =  'http://global.bing.com/search?%s' % data
        try:
            html = urlopen(url)
        except urllib.error.URLError as ex:
            print(ex)
            yield None
            first += 1
            continue
        bsObj = BeautifulSoup(html, 'html.parser')
        result = bsObj.find('li', {'class':'b_algo'})
        yield result.a['href']
        first += 1
        values = {
            'setmkt': 'en-us',
            'setlang': 'en-us',
            'q': word,
            'form': 'QBLH',
            'first': first*5
            }


def BFS(start, end):
    # Breath first search
    words_in_tree = [start]
    root = wordNode(start, '0', 'root')

    level = 0
    parent_list = [root]
    while level <= 6:
        next_parent_list = []
        level += 1
        print('\n\ncreating the level %d ....' % level)
        print('%d nodes in the parent level' % len(parent_list))
        for parentNode in parent_list:
            sys.stdout.write('**')
            sys.stdout.write(parentNode.get_word())
            sys.stdout.write('\n')
            sys.stdout.flush()
            # search neighbours
            # for url in wiki_bing_search(parentNode.get_word()):
            for url in bing_search(parentNode.get_word(), end):
                nei = find_neighbours_in_url(parentNode.get_word(), url)

                count = 0
                if not nei:
                    continue
                for node in nei:
                    if node.get_word() in words_in_tree:
                        continue
                    words_in_tree.append(node.get_word())
                    parentNode.add_child(node)
                    next_parent_list.append(node)
                    count += 1
                
                if end in [x.get_word() for x in nei]:
                    print('word ({}) has been found, and stop growing tree!'.format(
                        end))
                    endNode = [x for x in nei if x.get_word() == end][0]
                    path = show_path(root, endNode)
                    show_sentences(path)
                    return
        if level==1 and len(next_parent_list)==0:
            print('nothing found, reverse the words !')
            start, end = end, start
            print('start from ({}) to ({})'.format(start, end))
            words_in_tree = [start]
            root = wordNode(start, '0', 'root')
            level = 0
            parent_list = [root]
            level -= 1
        elif len(next_parent_list)==0:
            print('sorry, but I find nothing...')
            return
        else:
            print([x.get_word() for x in next_parent_list])
            parent_list = next_parent_list
    else:
        print('stop growing tree because of the level limit')
        return


def main(start=None, end=None):
    # input word for the start and the end
    if (not start) and (not end):
        while 1:
            start = input('the word to start:')
            end = input('the word to end:')
            if start.isalpha() and  end.isalpha():
                break
            print('Alphabel only !')

    # start searching
    BFS(start, end)

    print("Done !")


if __name__ == '__main__':
    main()
