import numpy as np
import pickle

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

with open('stc_weibo_train_post','r',encoding='utf8') as postFile,\
    open('stc_weibo_train_response','r',encoding='utf8') as responseFile,open('newkey.txt','w',encoding='utf8') as newkey,\
    open('newvalue.txt','w',encoding='utf8') as newvalue,open('test.txt','w',encoding='utf8') as testFile ,\
    open('testoutput.txt','w',encoding='utf8') as testoutputFile ,open('wordlist.json', 'wb') as wordlist:

    wordDict=dict()
    trainLen=4391599
    testLen=44359
    allLen=trainLen+testLen
    i=0

    for key,value in zip(postFile,responseFile):
        if i<trainLen:
            newkey.write(key)
            newvalue.write(value)
        else:
            testFile.write(key)
            testoutputFile.write(value)
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
    print('use:%f' % useNum*1.0/wordsSum)
    print('trainlen:%d' % trainLen)
    print('testlen:%d' % testLen)
    pickle.dump(newDict, wordlist)
