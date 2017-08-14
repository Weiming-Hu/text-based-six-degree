# this module defines a word_node class
#
#  word_node is used to represent a word in a text context
# for example a word_node in a text context should have the following:
# - word
# - sentence
# - url
# - friends
# - master
#
# word_nodes make up a tree
#
import sys
import re


class word_node:

    def __init__(self, word, sentence, url = None, friends = set(), master = None):
        # constructor

        # initial check
        at_middle = r"([^0-9A-Za-z]" + word + "[^0-9A-Za-z])"
        at_start = r"(^" + word + "[^0-9A-Za-z])"
        at_end = r"([^0-9A-Za-z]" + word + "$)"
        occur = re.findall(r"(" + at_start + "|" + at_middle + "|" + at_end + ")", sentence)
        if len(occur) == 0:
            sys.stderr.write('word_node initialization failed. word (%s) is not in sentence (%s)\n' %
                             (word, sentence))
            raise ValueError
        else:
            self._word = word
            self._sentence = sentence
            self._url = url
            self._friends = friends
            self._master = master

    def __str__(self):
        return "class wordNode: '{}' from '{}' ({}) having {} friends. Its master is '{}'".format(
            self._word, self._sentence, self._url, len(self._friends), self._master)

    def get_word(self):
        return self._word

    def get_sentence(self):
        return self._sentence

    def get_url(self):
        return self._sentence

    def get_master(self):
        return self._master

    def get_friends(self):
        return self._friends

    def set_friends(self, set_friends):
        if type(set_friends) is list:
            self._friends = set_friends
            self._friends.update()
        else:
            sys.stderr.write('friends should be a set. %s received.\n' % type(set_friends))

    def add_friends(self, new_friends):
        if type(new_friends) is str:
            # TODO
            # No, a new friend should be a word_node
            #
            self._friends.add(new_friends)
            self._friends.update()
        elif type(new_friends) is list:
            self._friends.union(set(new_friends))
            self._friends.update()
        elif type(new_friends) is set:
            self._friends.union(new_friends)
            self._friends.update()
        else:
            sys.stderr.write('friends should be a list, a set, or a single word string. %s received.\n' % type(new_friends))
        # TODO
        # after adding new friend, the added ones should change their master