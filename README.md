# Text-Based Six Degree Project

**Date of Start: May. 2016**

The purpose of this project is ot prove [Six Degrees of Seperation](https://en.wikipedia.org/wiki/Six_degrees_of_separation) using a text-based approach, rather than emails and other social network methods.

## Make Contributions

If you are interested in making any contributions, please contact [Weiming](weiming@psu.edu). Thank you!

## Quick Look

I propose that every English word is like a lively individual that is assigned with a meaning and can be used under different situations, and articles, news letters, academic papers, and so on, have formed a human-like society. Each word can be defined as a friend to its directly adjacent words. By studying the connection between any two words, I try to discover and prove Six Degree of Seperation.

Why do I study the Six Degree based on texts, rather on the real social network?

- First, it's interesting, and I can't tell the result just using my intuition;
- Second, I have already got enough spams and junk information in my mailbox. So I want our entertaining project to be smooth and quiet.

## Modules

##### find_path_local.py

I have prepared my own database out of novels to make a simple demo. The database is not included in the repository.

##### find_path_server.py

I think it would be more powerful and fun to do an online version. The basic algorithm has been completed, but I am actually having trouble deploying it on line. Feel interested ? Please contact me.

##### DataManagement_new.py

The main functions include :

1. format txt files;
2. convert pdf to txt files;
3. break formatted txt files into space-split sentences;
4. write formatted sentences into sqlite database;
5. check the database and delete empty tables;

Multiprocessing is used.

##### test.py

This is a unit test module.

##### pdf2txt.py#

This is copied from the third package, PDFminer, to convert PDF files to TXT files.

##### DataManagement_new.py

Deprecated.
