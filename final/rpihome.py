import time
import recognition
import news_crawer
import weather_crawer
import subprocess
import pexpect
import BLE
import util
import signal
import os
import RPi.GPIO as GPIO 
###
DEBUG = 0
cmd = ''
# wait, start_hearing
# craw_weather, craw_news
news_archive = {}
city_dict = {'台北':'Taipei_City', '台北市':'Taipei_City','基隆市':'Keelung_City', '新竹市':"Hsinchu_City", '新竹':"Hsinchu_City",'新北市':"New_Taipei_City",
             '桃園市':'Taoyuan_City', '新竹縣':'Hsinchu_County', '苗栗':'Miaoli_County','台中':'Taichung_City','彰化':"Changhua_County",
             '南投':'Nantou_County', '雲林':'Yunlin_County', '嘉義市':'Chiayi_City', '嘉義':'Chiayi_City', '嘉義縣':'Chiayi_County',
             '宜蘭':'Yilan_County', '花蓮':'Hualien_County', '台東':'Taitung_County', '台南':'Tainan_City', '高雄':'Kaohsiung_City', '屏東':'Pingtung_County',
             '連江':'Lienchiang_County', '金門':'Kinmen_County', '澎湖':'Penghu_County' }
fanDevice = None
SoundLevel = 15
CurrentTemp = None
###
def play_music_from_youtube(name):
    cmd = 'tizonia --youtube-audio-search {}'.format(name)
    # speaker = pexpect.spawn(cmd,logfile=None, searchwindowsize=200)
    speaker = subprocess.Popen(['tizonia', '--youtube-audio-search', name])
    time.sleep(60)
    print("it's time to kill process")
    speaker.send_signal(signal.SIGINT)

def getTempAndHumity():
    subprocess.call(['sudo', 'insmod', './dht11.ko'])
    tmp = str(subprocess.check_output(['sudo', 'cat', '/dev/DHT11']))
    tmp = tmp.split('\\n')
    hum = tmp[0][-5:-1]
    temp = tmp[1][-5:-1]
    sstr = "現在的氣溫為攝氏{}度，濕度為百分之{}".format(temp, hum)
    print(sstr)
    return sstr

def getTemp():
    subprocess.call(['sudo', 'insmod', './dht11.ko'])
    tmp = str(subprocess.check_output(['sudo', 'cat', '/dev/DHT11']))
    tmp = tmp.split('\\n')
    hum = tmp[0][-5:-1]
    temp = tmp[1][-5:-1]
    return float(temp)

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
    global news_archive
    global cmd
    global SoundLevel, CurrentTemp
    # getTempAndHumity()
    ### initialize
    fanDevice = BLE.BLEdevice()
    CurrentTemp = getTemp()
    util.ChangeSoundLevel(SoundLevel)
    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
    GPIO.setup(37, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
    ###
    print("Current temp is {}".format(CurrentTemp))
    print("initialize done")
    while True:
        print(">>>> command : {}".format(cmd))
        while True:
            if fanDevice.fanPower == 'on':
                tmpTemp = getTemp()
                if tmpTemp - CurrentTemp > 1.0:
                    os.system('mpv ./sounds/tempup.mp3')
                    fanDevice.speedUpFan()
                elif CurrentTemp - tmpTemp > 1.0:
                    os.system('mpv ./sounds/tempdown.mp3')
                    fanDevice.speedDownFan()

            ## listen
            if DEBUG:
                print("DEBUG is on, please type your command")
                cmd = input()
            else:
                cmd = recognition.rec()
            print("command is : ",cmd)
            if cmd == 0 :
                continue
            else :
                break
        if "天氣" in cmd:
            print(">>>> command : {}".format(cmd))
            for it in city_dict:
                if it in cmd:
                    sstr = weather_crawer.get_weather(it)
                    break
            recognition.t2speech(sstr)
            ## call craw_weather
        elif "現在" in cmd:
            if "時間" in cmd:
                sstr = getCTime()
                recognition.t2speech(sstr)
                cmd = ''
            elif "氣溫" in cmd or "溫度" in cmd or "溫濕度" in cmd:
                sstr = getTempAndHumity()
                recognition.t2speech(sstr)
                cmd = ''

        elif "新聞" in cmd:
            sstr = news_crawer.craw_hot()
            news_archive = sstr
            recognition.t2speech("以下為今日的熱門新聞")
            tmp = []
            for it in sstr:
                tmp.append(str(it['rank']) + '，' + it['title'])
                # recognition.t2speech("{}，，{}".format(it['rank'], it['title']))
            tmp = '，，'.join(tmp)
            recognition.t2speech(tmp)

        elif "關機" in cmd or "掰掰" in cmd:
            recognition.t2speech("掰掰")
            break
        elif "歌" in cmd:
            recognition.t2speech("請問你要播什麼歌")
            if DEBUG:
                print("DEBUG is on, please type your command")
                quer = input()
            else:
                quer = recognition.rec()
            print(quer)
            play_music_from_youtube(quer)
        elif "風扇" in cmd or "電扇" in cmd:
            if '打開' in cmd or '關' in cmd:
                fanDevice.fanPowerSwitch()
                sstr = None
            elif '強' in cmd or '快' in cmd:
                sstr = fanDevice.speedUpFan()
            elif '弱' in cmd or '慢' in cmd:
                sstr = fanDevice.speedDownFan()
            if sstr != None:
                recognition.t2speech(sstr)
        elif "大聲" in cmd:
            if SoundLevel != 25:
                SoundLevel +=5
                util.ChangeSoundLevel(SoundLevel)
            else:
                recognition.t2speech("已經是最大聲了")

        elif "小聲" in cmd:
            if SoundLevel != 5:
                SoundLevel -=5
                util.ChangeSoundLevel(SoundLevel)
            else:
                recognition.t2speech("已經是最小聲了")
        else:
            print("cmd is none of anyone")
            print("cmd :",cmd)
            os.system('mpv ./sounds/sayagain.mp3')
        cmd=''
        #time.sleep(1)

if __name__ == '__main__':
    main()
