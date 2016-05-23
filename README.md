#Text-based Six Degree Project

**Date: Mar. 2016**

This module is to prove the Six Degree theory on a text base.

##Get Involved

Hi there! Thank you for your concern. I have only finished the basic searching algorithms, and there are other things to be done. If you
- know how to deploy the project to any cloud,
- can think of a better searching algorithm or any other fun idea,
please contact me (Weiming @ the bottom of this page). I need your help !

##Quick Look

We hold the thoughts that every *(English)* word is like an individual and a set of articles, news letters, academic papers and so on, has formed a human-like society. Each word has a rather simple relationship with its two *(or just the preceding/following one if you like)* direct neighbors. By studying the connection between any two words, we try to demonstrate the Six Degree based on texts.

**Why do we study the Six Degree based on texts, rather on the real social network?**
- First, it's interesting, and actually we don't know the result;
- Secondly, we have already got enough spans and junk information, so we want our entertaining project to be smooth and quiet.

##Modules

#####find_path_local.py

I have prepared my own database out of novels to make a simple demo. The database is not included in the repository.

#####find_path_server.py

I think it would be more powerful and fun to do an online version. The basic algorithm has been completed, but I am actually having trouble deploying it on line. Feel interested ? Please contact me.

#####DataManagement_new.py

The main functions include :
1. format txt files;
2. convert pdf to txt files;
3. break formatted txt files into space-split sentences;
4. write formatted sentences into sqlite database;
5. check the database and delete empty tables;

Multiprocessing is used.

#####test.py

This is a unit test module.

#####pdf2txt.py#

This is copied from the third package, PDFminer, to convert PDF files to TXT files.

#####DataManagement_new.py

Deprecated.

##Contact##

- Weiming: [outlook](cosmos.weiming@outlook.com)
- Qi: [QQ](568817879@qq.com)
- Wen
