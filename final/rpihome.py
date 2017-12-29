import time
import recognition
import news_crawer
import weather_crawer
import subprocess
###
DEBUG = 1
state = 'wait'
cmd = ''
# wait, start_hearing
# craw_weather, craw_news
###            state = 'wait'

city_dict = {'台北市':'Taipei_City', '臺北市':'Taipei_City','基隆市':'Keelung_City', '新竹市':"Hsinchu_City",'新北市':"New_Taipei_City",
             '桃園市':'Taoyuan_City' }

def getTempAndHumity():
    subprocess.call(['sudo', 'insmod', './dht11.ko'])
    tmp = str(subprocess.check_output(['sudo', 'cat', '/dev/DHT11']))
    tmp = tmp.split('\\n')
    hum = tmp[0][-5:-1]
    temp = tmp[1][-5:-1]
    sstr = "現在的氣溫為攝氏{}度，濕度為百分之{}".format(temp, hum)
    print(sstr)
    return sstr

def getCTime():
    now = time.localtime()
    mon = now[1]
    date = now[2]
    hour = now[3]
    minute = now[4]
    if hour < 12:
        dn = '上午'
    elif hour == 12:
        dn = '下午'
    else:
        hour = hour - 12
        dn = '下午'
    rnt = "現在時間，{}月，{}日，{}，{}點，{}分".format(mon, date, dn, hour, minute)
    return rnt

def main():
    global state
    global cmd
    while True:
        print(">>>> state : {}".format(state))
        print(">>>> command : {}".format(cmd))
        while state == 'wait':
            ## listen
            cmd = recognition.rec()
            print("command is : ",cmd)
            if cmd == 0 :
                continue
            else :
                break
        if "天氣" in cmd:
            print(">>>> state : {}".format(state))
            print(">>>> command : {}".format(cmd))
            state = 'craw_weather'
            for it in city_dict:
                if it in cmd:
                    sstr = weather_crawer.get_weather(it)
                    break
            recognition.t2speech(sstr)
            state = 'wait'
            ## call craw_weather
        elif "現在" in cmd:
            if "時間" in cmd:
                state = 'getCTime'
                sstr = getCTime()
                recognition.t2speech(sstr)
                cmd = ''
                state = 'wait'
            elif "氣溫" in cmd or "溫度" in cmd or "溫濕度" in cmd:
                sstr = getTempAndHumity()
                recognition.t2speech(sstr)
                cmd = ''
                state = 'wait'

        elif "新聞" in cmd:
            state = "craw_news"
            sstr = news_crawer.craw_hot()
            recognition.t2speech("以下為今日的熱門新聞")
            tmp = []
            for it in sstr:
                tmp.append(str(it['rank']) + '，' + it['title'])
                # recognition.t2speech("{}，，{}".format(it['rank'], it['title']))
            tmp = '，，'.join(tmp)
            recognition.t2speech(tmp)
            state = 'wait'
        elif "播放" in cmd:
            state = "craw_music"
            state = 'wait'            
        elif "關機" in cmd or "掰掰" in cmd:
            recognition.t2speech("掰掰")
            break
        else:
            print("cmd is none of anyone")
            print("cmd :",cmd)
            recognition.t2speech('沒有這個指令')
            state = 'wait'  

        time.sleep(1)

if __name__ == '__main__':
    main()
