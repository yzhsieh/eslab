# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime
###
url = 'http://www.cwb.gov.tw/V7/forecast/'
query_weather = '臺北市'
# fill up the dict if have time
city_dict = {'台北市':'Taipei_City', '臺北市':'Taipei_City','基隆市':'Keelung_City', '新竹市':"Hsinchu_City",'新北市':"New_Taipei_City"
             '桃園市':'Taoyuan_City', }
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

def get_weather(name):
    city = city_dict[name]
    qurl = url + 'taiwan/' + city + '.htm'
    print(qurl)
    resp = requests.get(qurl)  
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    dom = soup.find("table",attrs={'class':"FcstBoxTable01"})
    tables = dom.find_all('tr')
    for item in tables:
        l= list()
        l.append(str(item.find('th').text).split(' ')[0])
        l.extend([ a.text for a in item.find_all('td')])
        if len(l) > 2:
            l.remove(l[2])
        print(l)
if __name__ == '__main__':
    get_weather("台北市")
    print(datetime.datetime.now().time)
    