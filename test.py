# this is the unitest file for Text-based Six Degree project

import sys
import unittest

from class_word_node import word_node

# define our test class
class test_word_node(unittest.TestCase):

    def test_init(self):
        success_count = 0
        word = 'test'
        sentences = ['Atest is at the start',
                     'End is the word testtest',
                     'End is the word testtest.',
                     'Word is burried in somethingtest',
                     'Word is burried in somethingtestsomething',
                     'Word is burried in testsomething',
                     'Word is duplicated like testtest.',
                     'Word is duplicated like testtest',
                     'This test should be good.',
                     'test should be good.',
                     'This should be a good test.',
                     'This should be a good test',
                     ]
        for s in sentences:
            try:
                wn = word_node(word, s)
            except ValueError as e:
                sys.stderr.write(e.message)
            else:
                success_count += 1
        self.assertEqual(success_count, 4)

if __name__ == "__main__":
    unittest.main()