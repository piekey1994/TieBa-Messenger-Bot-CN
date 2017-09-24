#coding:utf-8
import numpy as np
import pickle

with open('newkey.txt','w',encoding='utf8') as newkey,open('newvalue.txt','w',encoding='utf8') as newvalue ,open('wordlist.json', 'wb') as wordlist:
    newSet=set()
    conversationDictionary = np.load('conversationDictionary.npy').item()
    for key,value in conversationDictionary.items():
        newkey.write(key+'\n')
        newvalue.write(value+'\n')
        newSet = newSet | set(key.split()) | set(value.split())
    newDict=dict()
    i=0
    for word in newSet:
        newDict[word]=i
        i=i+1
    print(i)
    pickle.dump(newDict, wordlist)
