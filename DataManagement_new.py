#!/usr/bin/python
# -*- coding: utf-8 -*-
#===============================================================================
# This module creates the database to be used later.
# 
# SQLite is used.
# 
# table naming convention:
#     table_[pdf/txt][compact name] is the formal case
#===============================================================================

from multiprocessing import Process, Lock
import sqlite3
import pdf2txt
import os 
import sys
import re


def formatTXT():
    # format txt and save them under txt_fmt directory
    
    lock = Lock()
    fileList = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/txt")
    processPool = []
    for file in fileList:
        p = Process(target=formatTXT_thread,
                    args=("D:/EclipseWorkspace/TextbasedSixDegree/txt/" + file, lock))
        p.start()
        print("process started with id: %d" % p.pid)
        processPool.append(p)
    
    for p in processPool:
        p.join()
    
    print("Main process exits !")
    

def formatTXT_thread(fullpath, lock):
    if os.path.isfile("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/txt" + os.path.basename(fullpath)):
        with lock:
            print("process exits with id: %d " % os.getpid())
            return
        
    txt = open(fullpath, 'r')
    data = txt.read()
    data = data.replace("\f", '')
    data = data.replace('\n', ' ')
    data, number = re.subn(re.compile(" [ ]+"), " ", data)
    data, number = re.subn(re.compile("[^a-zA-Z. ]+"), "", data)
        
    txt_fmt = open("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/txt" + os.path.basename(fullpath), 'w')
    txt_fmt.write(data)
    
    txt.close()
    txt_fmt.close()


def convertPDF2TXT():
    # convert pdf to txt format and save it under txt_fmt directory
    
    lock = Lock()
    fileList = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/pdf")
    processPool = []
    for file in fileList:
        p = Process(target=convertPDF2TXT_thread,
                    args=("D:/EclipseWorkspace/TextbasedSixDegree/pdf/" + file, lock))
        p.start()
        print("process starts with id: %d " % p.pid)
        processPool.append(p)
    
    for p in processPool:
        p.join()
    
    print("Main process exits !")


def convertPDF2TXT_thread(fullpath, lock):
    # 0 conversion succeed and created new txt file
    # 1 failed
    # 2 already done and nothing has been changed
      
    _argv = ["D:/EclipseWorkspace/TextbasedSixDegree/pdf2txt.py",
             "-o", "D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-3] + "txt",
             fullpath]
    
    if os.path.isfile("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-3] + "txt"):
        with lock:
            print("process exits with id: %d " % os.getpid())
        return 2
    else:
        try:
            pdf2txt.main(_argv)
        except:
            print("PDF 2 TXT conversion failed. Info:")
            print(sys.exc_info()[1])
            with lock:
                print("process exits with id: %d " % os.getpid())
            return 1
    
    # format txt
    txt = open("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-3] + "txt", 'r')
    data = txt.read()
    data = data.replace("\f", '')
    data = data.replace('\n', ' ')
    data, number = re.subn(re.compile(" [ ]+"), " ", data)
    data, number = re.subn(re.compile("[^a-zA-Z. ]+"), "", data)    
    txt_fmt = open("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-4] + "_fmt.txt", 'w')
    txt_fmt.write(data)
    
    txt.close()
    txt_fmt.close()
    os.remove("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-3] + "txt")
    os.rename("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + os.path.basename(fullpath)[:-4] + "_fmt.txt",
              "D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/pdf" + os.path.basename(fullpath)[:-3] + "txt")
    
    with lock:
        print("process exits with id: %d " % os.getpid())
    return 0


def breakTXT(fullpath):
    # called by writeDB() when writing the database
    
    data = open(fullpath, 'r').read()
    sentenceList = data.split('.')
    sentenceList[:] = [i for i in sentenceList if len(i.split(' ')) >= 3]
    return sentenceList


def writeDB():
    # log information
    new = 0
    skipped = 0
    
    print('---------- writing database ----------')
    fileList = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt")
    conn = sqlite3.connect('sentences.sqlite')
    conn.text_factory = str
    cur = conn.cursor()
    for file in fileList:
        tableName, number = re.subn(re.compile("[^a-zA-Z0-9]+"), "", file[:-4])
        tableName = 'table_' + tableName
        if tableName in [i[0] for i in cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")] :
            print("table exists with name: %s" % tableName)
            skipped += 1
            continue
        # the first way to write database
        # cur.execute("DROP TABLE IF EXISTS %s" % tableName)
        cur.execute("CREATE TABLE %s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, content TEXT)" % tableName)
    
        sentenceList = breakTXT("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + file)
        for item in sentenceList:
            # there are still some extra spaces in the items, get rid of them
            item, number = re.subn(re.compile(" [ ]+"), "", item)
            # if there are spaces at the beginning, get rid of them
            item, number = re.subn(re.compile("^[ ]+"), "", item)
            # if there are spaces at the end, get rid of them
            item, number = re.subn(re.compile("[ ]+$"), "", item)
            
            if len(item.split(' ')) < 3: continue

            # the second way to write database
            sql = "INSERT INTO %s (content) VALUES ( ? )" % (tableName,)
            cur.execute(sql, (item,))
        conn.commit()
        new += 1
    
    conn.close()
    
    print('writing database done!')
    print('new table:\t %d' % new)
    print('files skipped:\t %d' % skipped)


def delete_empty_table():
    print("---------- deleting empty tables ----------")
    count = 0
    conn = sqlite3.connect('sentences.sqlite')
    conn.text_factory = str
    cur = conn.cursor()
    tableList = [i[0] for i in cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")]
    for name in tableList:
        data = cur.execute("SELECT * FROM " + name).fetchall()
        if not data:
            cur.execute("DROP TABLE " + name)
            count += 1
    conn.close()
    print("%d empty tables are deleted." % count)

    
if __name__ == '__main__':
#parameter tag:
#    1 ----- refresh database
#    2 ----- convert files in pdf folder
#    3 ----- convert files in txt folder
    tag = input("input tag: ")
    if (tag == 1):
        writeDB()
    elif (tag == 2):
        convertPDF2TXT()
        writeDB()
    elif (tag == 3):
        formatTXT()
        writeDB()
    else:
        print("No command for that tag.")
    delete_empty_table()
    
