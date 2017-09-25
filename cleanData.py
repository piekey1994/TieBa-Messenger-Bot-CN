#coding:utf-8

# 删除规则:
# 把句末和句首的非中文字符删除
# 删除所有emoji表情
# 删除长度小于2的
# 删除两句长度相差大于n(假设是20)
# 删除带有@的
# 删除带有网址的

import emoji
import numpy as np
import pickle

dos=20 #difference of sentence's length
tiebaName='王者荣耀'


def remove_emoji(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

newResult=dict()
oldResult = np.load(tiebaName+'.npy').item()
for k,v in oldResult.items():
	k = remove_emoji(k)
	while(len(k)>1):
		if u'\u4e00' <= k[-1] <= u'\u9fff':
			break
		else:
			k=k[:-1]
	while(len(k)>1):
		if u'\u4e00' <= k[0] <= u'\u9fff':
			break
		else:
			k=k[1:]
	if len(k)<2:
		continue
	v = remove_emoji(v)
	while(len(v)>1):
		if u'\u4e00' <= v[-1] <= u'\u9fff':
			break
		else:
			v=v[:-1]
	while(len(v)>1):
		if u'\u4e00' <= v[0] <= u'\u9fff':
			break
		else:
			v=v[1:]		
	if len(v)<2 or abs(len(k)-len(v)) >= dos or k.find('@')!=-1 or v.find('@')!=-1 or k.find('http')!=-1 or v.find('http')!=-1:
		continue	
	newResult[k]=v

with open(tiebaName+'clean.txt','w',encoding='utf8') as converFile:#, open("wordList.txt", "wb") as fp:
	strSet=set()
	spiltResult=dict()
	for d,x in newResult.items():
		strSet=strSet | set(d+x)
		
		#d=' '.join(i for i in d)
		#x=' '.join(i for i in x)
		spiltResult[d]=x
		converFile.write(d+"\n"+x+"\n\n")
	print('对话组总数：'+str(len(newResult)))
	print('字符总数：'+str(len(strSet)))
	#pickle.dump(list(strSet), fp)
	np.save('conversationDictionary.npy', spiltResult)