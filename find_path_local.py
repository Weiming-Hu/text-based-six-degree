# find_path_local.py
# this script will find the connecion between two input words and print their
# intermedia nodes, within sentences.sqlite database

import sqlite3
import pdb
import re
import sys


class wordNode:
    def __init__(self, word: str, contentId: int, table: str):
        # these attributes are requied
        self._word = word
        self._contentId = contentId
        self._table = table
        self.children = []
        self.parent = None

    def __str__(self):
        return 'class wordNode: {} in table<{}> with id {}'.format(
            self._word,
            self._table,
            self._contentId)

    def get_word(self):
        return self._word

    def get_content_id(self):
        return self._contentId

    def get_table_name(self):
        return self._table

    def add_child(self, newNode):
        self.children.append(newNode)
        newNode.parent = self

def show_sentences(path, cur):
    for node in path:
        if not node.parent:
            continue
        cur.execute('SELECT content from {tableName} WHERE id = {contentId}'.format(
            tableName = node.get_table_name(),
            contentId = node.get_content_id()))
        s = cur.fetchone()[0]
        print(s)
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
        print('({word}) with id ({sentenceId}) in ({table})'.format(
            word=node.get_word(),
            sentenceId=node.get_content_id(),
            table=node.get_table_name()
            ))
    print('intermediates: %d' % (len(reverse_path) - 2))
    print('--------------------------------------\n')
    return reverse_path


def find_neighbours_in_one_sentence(target, s, tName, sId):
    # tName and sId will be used to initialize the wordNode class
    nei = []
    # some cleaning
    s, number = re.subn(re.compile('[ ][ ]+'), ' ', s)
    s, number = re.subn(re.compile('[ ]$'), '', s)
    s, number = re.subn(re.compile('^[ ]'), '', s)
    words = s.split(' ')
    assert '' not in words
    # find the neighbours
    for i in range(0, len(words)):
        if words[i].lower() == target.lower():
            tmp = words[i-1 if i>0 else 0 : i+2]
            tmp.remove(words[i])
            for word in tmp:
                new = wordNode(
                        word=word,
                        contentId=sId,
                        table=tName)
                nei.append(new)
    if nei:
        return nei
    else:
        return None


def find_all_neighbours(target, cur):
    # find all the neighbours of the target word
    # within the whole database
    found = []
    for tablename in [i[0] for i in cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")]:
        try:
            cur.execute('SELECT id, content from {tablename}'.format(tablename=tablename))
        except sqlite3.OperationalError:
            continue
        content = cur.fetchall()
        for line in content:
            # be aware that line is a tuple with two elements
            if target.lower() in line[1].lower():
                nei = find_neighbours_in_one_sentence(target, line[1], tablename, line[0])
                if nei:
                    found.extend(nei)
    return found


def BFS(start, end):
    # Breadth first search
    # connect database
    conn = sqlite3.connect('sentences.sqlite')
    cur = conn.cursor()

    # words_in_tree is used to eliminate duplication
    words_in_tree = [start]

    # create root wordNode
    root = wordNode(start, '0', 'root')

    # start loop search
    level = 0
    parent_list = [root]
    while level <= 6:
        next_parent_list = []
        level += 1
        print('\n\ncreating the level %d....' % level)
        print('%d nodes in the parent level' % len(parent_list))
        for parentNode in parent_list:
            sys.stdout.write('.')
            sys.stdout.flush()
            # search neighbours
            nei = find_all_neighbours(parentNode.get_word(), cur)

            # add children
            count = 0
            for node in nei:
                if node.get_word() in words_in_tree:
                    continue
                words_in_tree.append(node.get_word())
                parentNode.add_child(node)
                next_parent_list.append(node)
                count += 1
            # if end word already found
            if end in [x.get_word() for x in nei]:
                print('word ({}) has been found, and stop growing tree!'.format(
                    end))
                endNode = [x for x in nei if x.get_word() == end][0]
                path = show_path(root, endNode)
                show_sentences(path, cur)
                return
        parent_list = [x for x in next_parent_list]
    else:
        print('stop growing tree because of the level limit')
        return


def DFS(start, end):
    pass


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


if __name__ == "__main__":
    main()
