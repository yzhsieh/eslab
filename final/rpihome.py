import time
import recognition
import news_crawer
import weather_crawer
###
DEBUG = 1
state = 'wait'
cmd = ''
# wait, start_hearing
# craw_weather, craw_news
###            state = 'wait'

city_dict = {'台北市':'Taipei_City', '臺北市':'Taipei_City','基隆市':'Keelung_City', '新竹市':"Hsinchu_City",'新北市':"New_Taipei_City",
             '桃園市':'Taoyuan_City' }


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
        if state == 'wait':
            ## listen
            cmd = recognition.rec()
            print("command is : ",cmd)
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
            state = 'getCTime'
            sstr = getCTime()
            recognition.t2speech(sstr)
            cmd = ''
            state = 'wait'
        elif "新聞" in cmd:
            state = "craw_news"
            state = 'wait'
        elif "播放" in cmd:
            state = "craw_music"
            state = 'wait'            
        else:
            print("cmd is none of anyone")
            print("cmd :",cmd)
            recognition.t2speech('沒有這個指令')
            state = 'wait'  

        time.sleep(1)

if __name__ == '__main__':
    main()