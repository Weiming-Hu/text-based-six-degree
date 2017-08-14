#!/usr/bin/python
# -*- coding: utf-8 -*-
# functions
import re

def find_neighbors_in_sentence(target, s, case_sensitive=True):
    # find the neighbors in the sentence and return them in a list
    #
    # if strick is True, the function try to find the exact match
    # for the target word without changing cases
    #
    neis = []

    # some cleaning
    s, number = re.subn(re.compile('[ ][ ]+'), ' ', s)
    s, number = re.subn(re.compile('[ ]$'), '', s)
    s, number = re.subn(re.compile('^[ ]'), '', s)

    # match the target word(s) and its previous/following neighbors
    pairs = []
    if case_sensitive:
        # strict match mode:
        pairs = re.findall(r"([a-zA-Z]+) " + target + r" ([a-zA-Z]+)", s)
    else:
        pairs = re.findall(r"([a-zA-Z]+) " + target.lower() + r" ([a-zA-Z]+)", s.lower())

    for pair in pairs:
        for word in pair:
            neis.append(word)

    return neis