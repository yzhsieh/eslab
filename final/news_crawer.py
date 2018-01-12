# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import json
import datetime
import recognition
###
url = 'https://tw.appledaily.com/daily'
hot_news = []
###

def dom2csv(table,dep):
    rnt = []
    for item in table:
        tmp = []
        col = item.find_all('td')
        tmp.append(dep)
        tmp.append(col[2].text)
        tmp.append(col[3].text)
        tmp.append(col[4].text)
        # print(tmp)
        rnt.append(tmp)
    return rnt

def find_dep_list():
    global dep_list
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    dom = soup.find("select")
    tmp_list = dom.find_all("option")
    for item in tmp_list:
        dep_list.append(item.text)
    # print(dep_list)

def craw_hot(num = 10):
    resp = requests.get("https://tw.appledaily.com/hot/daily")  
    # resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    dom = soup.find('ul',attrs={'class':'all'})
    cnt = 1
    for item in dom.find_all('li'):
        tdom = item.find_all('div')[1]
        tmp = {}
        tmp['rank'] = cnt
        cnt += 1
        tmp['title'] = tdom.a.text
        tmp['href'] = tdom.a['href']
        hot_news.append(tmp)
        if cnt == num:
            break
    # dom = soup.find("table",attrs={'class':"FcstBoxTable01"})

    for a in hot_news:
        print("{:2d} : {}".format(a['rank'], a['title']))
        resp = requests.get(a["href"])
        soup = BeautifulSoup(resp.text, 'html5lib')
        dom = soup.find('div',attrs={'class':'ndArticle_margin'})
        if dom == None:
            dom = soup.find('div',attrs={'class':'articulum'})
        dom = dom.find_all(['p', 'h2'])
        tmp = []
        for item in dom:
            if item.text != '':
                tmp.append(item.text.replace('\n',''))

        alltext = '。'.join(tmp)
        # for text in tmp:
            # text.replace('\\n','')

        a['article'] = alltext
    print("Crawl hot news done!!!")
    ## return format : 
    #   all news in a dict
    #   {'rank','title','href','article'}
    return hot_news

if __name__ == '__main__':
    sstr = craw_hot(2)
    print(sstr[0]['article'])
    recognition.t2speech(sstr[0]['article'])
