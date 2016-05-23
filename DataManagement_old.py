#===============================================================================
# This module creates the database to be used later.
# The database is designed to have single sentences as items labeled according to their file names.
# SQLite is used.
#===============================================================================

import sqlite3
import pdf2txt
import os 
import sys
import re


def convertPDF(fullpath):
    # read and convert the file to pure texts
    # 0 conversion succeed and created new txt file
    # 1 failed
    # 2 already done and nothing has been changed
    
    _argv = ["D:/EclipseWorkspace/TextbasedSixDegree/pdf2txt.py",
             "-o", "D:/EclipseWorkspace/TextbasedSixDegree/txt_ori/" + os.path.basename(fullpath)[:-3] + "txt",
             fullpath]
    if os.path.isfile("D:/EclipseWorkspace/TextbasedSixDegree/txt_ori/" + os.path.basename(fullpath)[:-3] + "txt"):
        return 2
    else:
        try:
            pdf2txt.main(_argv)
        except:
            print("PDF 2 TXT conversion failed. Info:")
            print(sys.exc_info()[1])
            return 1
    return 0


def convertDOC(fullpaht):
    pass


def convertHTM(fullpath):
    pass


def formatTXT():
    
    # get formatList that contains the files to be formatted
    formatList = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/txt_ori")
    txt_fmt_list = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt")
    for file in txt_fmt_list:
        if file in formatList:
            formatList.remove(file)
    
    # format txt files
    for file in formatList:
        data = open("D:/EclipseWorkspace/TextbasedSixDegree/txt_ori/" + file, 'r').read()
        
        # data formatting
        data = data.replace("\f", '')
        data = data.replace('\n', ' ')
        data, number = re.subn(re.compile(" [ ]+"), " ", data)
        
        open("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + file, 'w').write(data)
    return 0


def breakTXT(fullpath):
    data = open(fullpath).read()
    sentenceList = data.split('.')
    return sentenceList
    

def writeDB():
    fileList = os.listdir("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt")
    conn = sqlite3.connect('sentences.sqlite')
    conn.text_factory = str
    cur = conn.cursor()
    try:
        cur.execute('''
        CREATE TABLE dump (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            content TEXT);
        ''')
    except:
        pass
    
    for file in fileList:
        sentenceList = breakTXT("D:/EclipseWorkspace/TextbasedSixDegree/txt_fmt/" + file)
        for item in sentenceList:
            cur.execute("INSERT INTO dump (content) VALUES ( ? )", (item[1:] if item[0]==' ' else item,))
        conn.commit()
    
    return 0


def checkFormat(fullpath):
    # check and return the file format
    tag = os.path.basename(fullpath).split('.')[1]
    if tag == 'pdf':
        convertPDF(fullpath)
    elif tag in ['doc', 'docx']:
        convertDOC(fullpath)
    elif tag in ['txt', 'TXT']:
        pass
    elif tag in ['html', 'htm']:
        convertHTM(fullpath)
    else:
        print("sorry, I don't recognize " + tag +" format.")


def main(argv):
    pass
    
if __name__ == '__main__':
    pass