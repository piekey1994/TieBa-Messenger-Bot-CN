#!/usr/bin/env python  
import jieba
class NGram(object):  
  
    def __init__(self, n):  
        # n is the order of n-gram language model  
        self.n = n  
        self.unigram = {}  
        self.bigram = {}  
  
    # scan a sentence, extract the ngram and update their  
    # frequence.  
    #  
    # @param    sentence    list{str}  
    # @return   none  
    def scan(self, sentence):  
        # file your code here  
        for line in sentence:  
            self.ngram(line)  
        #unigram  
        if self.n == 1:  
            try:  
                fip = open("test_file/data.uni","w",encoding='utf-8')  
            except:  
                print >> sys.stderr ,"failed to open data.uni"  
            for i in self.unigram:  
                fip.write("%s %d\n" % (i,self.unigram[i]))  
        if self.n == 2:  
            try:  
                fip = open("test_file/data.bi","w",encoding='utf-8')  
            except:  
                print >> sys.stderr ,"failed to open data.bi"  
            for i in self.bigram:  
                fip.write("%s %d\n" % (i,self.bigram[i]))  
    # caluclate the ngram of the words  
    #  
    # @param    words       list{str}  
    # @return   none  
    def ngram(self, words):  
        # unigram  
        if self.n == 1:  
            for word in words:  
                if word not in self.unigram:  
                    self.unigram[word] = 1  
                else:  
                    self.unigram[word] = self.unigram[word] + 1  
  
        # bigram  
        if self.n == 2:  
            num = 0  
            stri = ''  
            for i in words:  
                num = num + 1  
                if num == 2:  
                    stri  = stri + " "  
                stri = stri + i  
                if num == 2:  
                    if stri not in self.bigram:  
                        self.bigram[stri] = 1  
                    else:  
                        self.bigram[stri] = self.bigram[stri] + 1  
                    num = 0  
                    stri = ''  
  
if __name__=="__main__":  
    import sys  
    fip = open('test_file/baiduqaclean2.txt',"r",encoding='utf-8')  
    sentence = []  
    for line in fip:  
        if len(line.strip())!=0:  
            sentence.append(jieba.cut(line.strip()))
    uni = NGram(1)  
    bi = NGram(2)  
    uni.scan(sentence)  
    bi.scan(sentence)  