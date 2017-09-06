#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import time
import traceback
import socket  
import myLog
import numpy as np

tiebaName='王者荣耀'
tiebaHtml='https://tieba.baidu.com/f?kw=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80&ie=utf-8&tab=good'

socket.setdefaulttimeout(15) #http请求超时时间
logger=myLog.getLogging(tiebaName+'log.txt') #log文件

def filterFun(tagname,flist): #多值class过滤器
    def listinlist(a,b):
        if(type(b)!=list):
            return False
        for i in a:
            if i not in b:
                return False
        return True
    return lambda tag: tag.name==tagname and  listinlist(flist,tag.get('class'))

with open(tiebaName+'.txt','w',encoding='utf8') as result:
    try:
        html=tiebaHtml
        resultDict=dict()
        while (True):
            logger.warning('读取主页面:'+html)
            try:
                bsObj = BeautifulSoup(urlopen(html),'lxml',from_encoding="utf-8")
            except:
                logger.warning('无法获取主页面'+html+' 10秒后重新获取')
                time.sleep(10)
                bsObj = BeautifulSoup(urlopen(html),'lxml',from_encoding="utf-8") 
                logger.warning('获取主页面'+html+'成功') 
            postlist=bsObj.find('ul',{'id':'thread_list'}).find_all(filterFun('li',['j_thread_list','clearfix'])) #获取帖子列表
            for post in postlist:
                #print(post.prettify())
                posthref=post.find(filterFun('div',['threadlist_lz','clearfix'])).div.a.attrs["href"]
                if posthref.find('?')!=-1:
                    posthref=posthref[:posthref.find('?')]
                tid=posthref[posthref.rfind('/')+1:]
                while(True):
                    if posthref.find("https://tieba.baidu.com") == -1:
                        posthref="https://tieba.baidu.com"+posthref
                    #print(posthref)
                    try:
                        try:
                            postBs = BeautifulSoup(urlopen(posthref),'lxml',from_encoding="utf-8")
                        except:
                            logger.warning('无法获取帖子页面'+posthref+' 10秒后重新获取')
                            time.sleep(10)
                            postBs = BeautifulSoup(urlopen(posthref),'lxml',from_encoding="utf-8")
                            logger.warning('获取帖子页面'+posthref+'成功')
                        logger.info('开始爬取帖子页:'+posthref)
                        floorlist=postBs.find('div',{'class':'p_postlist','id':'j_p_postlist'}).find_all(filterFun('div',['l_post','l_post_bright','j_l_post','clearfix'])) #读取楼层
                        for floor in floorlist:
                            if floor.find('span',{'style':'display:','class':'lzl_link_fold'}) != None :
                                if floor.find(filterFun('div',['d_post_content','j_d_post_content']))==None:
                                    print(floor.prettify())
                                postcontent=re.sub('[\t\r\n\s]','',floor.find(filterFun('div',['d_post_content','j_d_post_content'])).get_text())
                                #print(postcontent)
                                pid=json.loads(floor.attrs['data-field'])['content']['post_id']
                                postValue=None
                                if len(postcontent)>0 and len(postcontent)<50 :
                                    replyDict=dict()
                                    replyPageNum=1
                                    firstReplyHtml='https://tieba.baidu.com/p/comment?tid='+tid+'&pid='+str(pid)+'&pn=1'
                                    try:
                                        replysBs =  BeautifulSoup(urlopen(firstReplyHtml),'lxml',from_encoding="utf-8")
                                    except:
                                        logger.warning('无法获取评论页面'+firstReplyHtml+' 5秒后重新获取')
                                        time.sleep(5)
                                        replysBs =  BeautifulSoup(urlopen(firstReplyHtml),'lxml',from_encoding="utf-8")
                                        logger.warning('获取评论页面'+firstReplyHtml+'成功')
                                    #print(replysBs.prettify())
                                    pageA = replysBs.find(filterFun('p',['j_pager','l_pager','pager_theme_2']))
                                    #print(pageA)
                                    if pageA != None and len(pageA.find_all('a'))!=0:
                                        replyPageNum=pageA.find_all('a')[-1].attrs['href'][1:]
                                    #print(replyPageNum)
                                    for i in range(1,int(replyPageNum)+1):
                                        replyHtml='https://tieba.baidu.com/p/comment?tid='+tid+'&pid='+str(pid)+'&pn='+str(i)
                                        try:
                                            replysBs =  BeautifulSoup(urlopen(replyHtml),'lxml',from_encoding="utf-8")
                                        except:
                                            logger.warning('无法获取评论页面'+replyHtml+' 5秒后重新获取')
                                            time.sleep(5)
                                            replysBs =  BeautifulSoup(urlopen(replyHtml),'lxml',from_encoding="utf-8")
                                            logger.warning('获取评论页面'+replyHtml+'成功')
                                        replys=replysBs.find_all('div',{'class':'lzl_cnt'})
                                        for reply in replys:
                                            username=reply.a.get_text()
                                            replycontent=re.sub('[\t\r\n\s]','',reply.span.get_text())
                                            replyFlag=False
                                            if replycontent.find('回复') == 0 and (replycontent.find(':') != -1 or replycontent.find('：') != -1):
                                                if  reply.span.find('a') != None:
                                                    if replycontent.find(':') != -1:
                                                        replycontent=replycontent[replycontent.find(':')+1:]
                                                    else:
                                                        replycontent=replycontent[replycontent.find('：')+1:]
                                                    replyFlag=True
                                                else:
                                                    continue
                                            if len(replycontent)>0 and len(replycontent)<50:
                                                replyDict[username]=replycontent
                                                if replyFlag:
                                                    replyname=reply.span.find('a').get_text().replace('@','')
                                                    if replyname in replyDict.keys():
                                                        resultDict[replyDict[replyname]]=replycontent 
                                                        
                                                else:
                                                    if postValue == None or abs(len(postValue)-len(postcontent)) > abs(len(replycontent)-len(postcontent)):
                                                        postValue=replycontent
                                                        resultDict[postcontent]=replycontent
                        postPagesLi=postBs.find(filterFun('li',['l_pager','pager_theme_5','pb_list_pager']))
                        if postPagesLi != None:
                            postPages= postPagesLi.find_all('a')
                            if len(postPages)>0 and postPages[-2].get_text() == '下一页':
                                posthref=postPages[-2].attrs['href']
                                postpagenum=int(posthref[posthref.find('=')+1:])
                                if(postpagenum>300):
                                    break
                            else:
                                break
                        else:
                            break
                    except:
                        logger.error(traceback.format_exc())
                        break
                logger.info('完成帖子:'+posthref+';当前对话总数为:'+str(len(resultDict)))
            nextPage=bsObj.find(filterFun('a',['next','pagination-item']))
            if nextPage != None:
                html='https:'+nextPage.attrs['href']
            else:
                break
        np.save(tiebaName+'.npy', resultDict)
        for d,x in resultDict.items():
            result.write(d+"\t"+x+"\n")   
        logger.warning('成功抓取所有帖子!')
    except:
        logger.error(traceback.format_exc())
        np.save(tiebaName+'.npy', resultDict)
        for d,x in resultDict.items():
            result.write(d+"\t"+x+"\n")
        logger.warning('部分帖子抓取失败，已为您保存文件!')                                  