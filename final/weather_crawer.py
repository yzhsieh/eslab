# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import json
import datetime
###
url = 'http://www.cwb.gov.tw/V7/forecast/'
query_weather = '臺北市'
# fill up the dict if have time
city_dict = {'台北':'Taipei_City', '台北市':'Taipei_City','基隆市':'Keelung_City', '新竹市':"Hsinchu_City", '新竹':"Hsinchu_City",'新北':"New_Taipei_City",
             '桃園市':'Taoyuan_City', '新竹縣':'Hsinchu_County', '苗栗':'Miaoli_County','台中':'Taichung_City','彰化':"Changhua_County",
             '南投':'Nantou_County', '雲林':'Yunlin_County', '嘉義市':'Chiayi_City', '嘉義':'Chiayi_City', '嘉義縣':'Chiayi_County',
             '宜蘭':'Yilan_County', '花蓮':'Hualien_County', '台東':'Taitung_County', '台南':'Tainan_City', '高雄':'Kaohsiung_City', '屏東':'Pingtung_County',
             '連江':'Lienchiang_County', '金門':'Kinmen_County', '澎湖':'Penghu_County' }
###


def get_weather(name):
    city = city_dict[name]
    qurl = url + 'taiwan/' + city + '.htm'
    print(qurl)
    resp = requests.get(qurl)  
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    dom = soup.find("table",attrs={'class':"FcstBoxTable01"})
    tables = dom.find_all('tr')
    weat_res = []
    for item in tables:
        l= list()
        l.append(str(item.find('th').text).split(' ')[0])
        l.extend([ a.text for a in item.find_all('td')])
        if len(l) > 2:
            l.remove(l[2])
        weat_res.append(l)
        print(l)
    rnt = []
    rnt.append( "{}的天氣預報如下".format(weat_res[0][0]) )
    weat_res.remove(weat_res[0])
    for item in weat_res:
        temperature = item[1].split(' ')
        temperature = [temperature[0],temperature[2]]
        rainrate = item[3].split(' ')[0]
        mystr = "{}的氣溫為{}到{}度，降雨機率為百分之{}".format(item[0],temperature[0],temperature[1],rainrate)
        # print(mystr)
        rnt.append( mystr )
    rnt = '，'.join(rnt)
    print('\n',rnt)
    return rnt
if __name__ == '__main__':
    get_weather("高雄")
    