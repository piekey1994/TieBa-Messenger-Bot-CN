import numpy as np
import pickle

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

dos=20 #difference of sentence's length
minlen=4

with open('baiduqa.txt','r',encoding='utf8') as oldResult,open('baiduqaclean.txt','w',encoding='utf8') as converFile:

    newResult=dict()
    for line in oldResult:
        k=line.split('\t')[0]
        v=line.split('\t')[1][:-1]
        if len(v)<minlen or abs(len(k)-len(v)) >= dos:
            continue	
        newResult[k]=v
    strSet=set()
    spiltResult=dict()
    for d,x in newResult.items():
        strSet=strSet | set(d+x)
		
        spiltResult[d]=x
        converFile.write(d+"\n"+x+"\n\n")
    print('对话组总数：'+str(len(newResult)))
    print('字符总数：'+str(len(strSet)))
    #pickle.dump(list(strSet), fp)
    np.save('conversationDictionary.npy', spiltResult)