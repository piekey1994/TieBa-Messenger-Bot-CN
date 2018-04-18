#coding:utf-8
import numpy as np
import pickle
import jieba
with open('newkey.txt','w',encoding='utf8') as newkey,open('newvalue.txt','w',encoding='utf8') as newvalue,open('test.txt','w',encoding='utf8') as testFile ,\
open('testoutput.txt','w',encoding='utf8') as testoutputFile ,open('wordlist.json', 'wb') as wordlist:
    newSet=set()
    conversationDictionary = np.load('conversationDictionary.npy').item()
    allLen=len(conversationDictionary.items())
    testLen=allLen*0.01
    trainLen=allLen-testLen
    i=0

    for key,value in conversationDictionary.items():
        key=' '.join(jieba.cut(key))
        value=' '.join(jieba.cut(value))
        if i<trainLen:
            newkey.write(key+'\n')
            newvalue.write(value+'\n')
            newSet = newSet | set(key.split()) | set(value.split())
        else:
            testFile.write(key+'\n')
            testoutputFile.write(value+'\n')
        i += 1
    newDict=dict()
    i=0
    for word in newSet:
        newDict[word]=i
        i=i+1
    print('wordnum:%d\n' % i)
    print('trainlen:%d\n' % trainLen)
    print('testlen:%d\n' % testLen)
    pickle.dump(newDict, wordlist)
