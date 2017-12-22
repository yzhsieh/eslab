import time
import recognition

###
state = 'wait'
cmd = ''
# wait, start_hearing
# craw_weather, craw_news
###
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
    rnt = "現在時間，{}月{}日，{}{}點{}分".format(mon, date, dn, hour, minute)
    return rnt

def main():


if __name__ == '__main__':
    while Ture:
        if state = 'wait':
            ## listen
            cmd = recognition.rec()
        if "天氣" in cmd:
            state = 'craw_weather'
            ## call craw_weather
        elif "時間" in cmd:
            state = 'getCTime'
            sstr = getCTime()
            ## call speak api
        elif "新聞" in cmd:
            state = "craw_news"