#coding:utf-8
import jieba

with open('testKey.txt','r',encoding='utf8') as keyFile,open('test.txt','w',encoding='utf8') as testFile:
    for line in keyFile:
        testFile.write(' '.join(jieba.cut(line)))