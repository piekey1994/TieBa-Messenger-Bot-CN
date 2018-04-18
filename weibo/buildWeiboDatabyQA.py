import numpy as np
import pickle
import jieba

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

with open('weibo.noqa.txt','r',encoding='utf8') as qaFile,open('newkey.txt','w',encoding='utf8') as newkey,\
    open('newvalue.txt','w',encoding='utf8') as newvalue,open('test.txt','w',encoding='utf8') as testFile ,\
    open('testoutput.txt','w',encoding='utf8') as testoutputFile ,open('wordlist.json', 'wb') as wordlist:

    wordDict=dict()
    trainLen=200000
    testLen=10000
    allLen=trainLen+testLen
    i=0

    for line in qaFile:
        if i==allLen:
            break
        key=' '.join(jieba.cut(line[:-1].split('\t')[0]))
        value=' '.join(jieba.cut(line[:-1].split('\t')[1]))
        if i<trainLen:
            newkey.write(key+'\n')
            newvalue.write(value+'\n')
        else:
            testFile.write(key+'\n')
            testoutputFile.write(value+'\n')
        for word in key.split():
            if word not in wordDict:
                wordDict[word]=1
            else:
                wordDict[word]+=1
        for word in value.split():
            if word not in wordDict:
                wordDict[word]=1
            else:
                wordDict[word]+=1
        i += 1
        if i%1000==0:
            print("finish:%d(%f)" % (i,i*1.0/allLen))
    wordDict=sorted(wordDict.items(),key = lambda x:x[1],reverse = True)
    newDict=dict()
    i=0
    wordsSum=0
    useNum=0
    for word in wordDict:
        if i<40000:
            newDict[word[0]]=i
            wordsSum += word[1]
            useNum += word[1]
        else:
            wordsSum += word[1]
        i=i+1
    print('wordsSum:%d' % i)
    print('use:%f' % (useNum/wordsSum))
    print('trainlen:%d' % trainLen)
    print('testlen:%d' % testLen)
    pickle.dump(newDict, wordlist)
