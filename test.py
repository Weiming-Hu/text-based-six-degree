# this is the unitext file for Text-based Six Degree project

import unittest
import sqlite3
from find_path_local import *


# define our test class
class test_find_path_py(unittest.TestCase):
    def setUp(self):
        # do some initialization
        # since all the tests below are independent
        # setUp() will be called every time before a new test
        self.conn = sqlite3.connect('sentences.sqlite')
        self.cur = self.conn.cursor()
        pass

    def tearDown(self):
        # do some cleaning after the test
        # tearDown() will be called every time after a test
        self.conn.close()
        pass

    def test_buttons_should_be_direct_neighbour_of_sparkled(self):
        # 'buttons sparkled' is at the middle of the sentence
        nei = find_all_neighbours('buttons', self.cur)
        found_words = [x.get_word() for x in nei]
        self.assertTrue('sparkled' in found_words)

    def test_dombey_should_be_direct_neighbour_of_exulting(self):
        # 'Dombey exulting' is at the start of the sentence
        nei = find_all_neighbours('Dombey', self.cur)
        found_words = [x.get_word() for x in nei]
        self.assertTrue('exulting' in found_words)

    def test_manner_should_be_direct_neighbour_of_becoming(self):
        # 'becoming manner' is at the end of the sentence
        nei = find_all_neighbours('manner', self.cur)
        found_words = [x.get_word() for x in nei]
        self.assertTrue('becoming' in found_words)

    def test_case_insensitivity_of_find_neighbours_in_one_sentence(self):
        # fp.find_neighbours_in_one_sentence() is case insensitive
        nei = find_neighbours_in_one_sentence(
                'lOVe',
                'So when people talk about love they think of passion and the LOVE of the nature',
                'table_name',
                10)
        found_words = [x.get_word() for x in nei]
        self.assertTrue('they' in found_words)
        self.assertTrue('about' in found_words)
        self.assertTrue('of' in found_words)

    def test_case_insensitivity_of_find_all_neighbours(self):
        # fp.find_all_neighbours() is case insensitive
        nei = find_all_neighbours('RaCKFulL', self.cur)
        found_words = [x.get_word() for x in nei]
        self.assertTrue('of' in found_words)

    def test_show_path_manually(self):
        # create a tree and then call show_path()
        # the path should be test -> end -> party
        root = wordNode('test', 0, 'table_root')
        root.add_child(wordNode('a', 12, 'table_a'))
        root.add_child(wordNode('the', 2, 'table_the'))
        root.add_child(wordNode('use', 7, 'table_use'))
        parent = wordNode('end', 9, 'table_use')
        root.add_child(parent)
        parent.add_child(wordNode('never', 14, 'table_never'))
        child = wordNode('party', 5, 'table_party')
        parent.add_child(child)
        show_path(root, child)

    def test_sentence_id_is_int(self):
        # the sentenceId of wordNode should be an int
        # which is been created by the database connection cur
        tablename = 'table_pdf11TheKoran'
        self.cur.execute('SELECT id, content from {tablename}'.format(tablename=tablename))
        one = self.cur.fetchone()
        self.assertTrue(isinstance(one[0], int))


if __name__ == "__main__":
    unittest.main()
