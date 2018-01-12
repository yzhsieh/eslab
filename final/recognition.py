#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import os
from os import path
import speech_recognition as sr
from gtts import gTTS
import audioop
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering


def rec():
    GPIO.setup(37, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Say something!')
        GPIO.output(37,True) ## Turn on GPIO pin 7
        audio = r.listen(source)
        

    try:
        sttTXT_org = r.recognize_google(audio, language = 'zh-TW')
        print("Google Speech Recognition thinks you said: " + sttTXT_org)
        GPIO.output(37,False)## Switch off pin 7
        return sttTXT_org
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        GPIO.output(37,False)## Switch off pin 7
        return 0
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
        GPIO.output(37,False)## Switch off pin 7
        return 0

def t2speech(txt):
    tts =  gTTS(text=txt,lang='zh-TW')
    tts.save('temp.mp3')
    os.system('mpv temp.mp3')
    os.remove('temp.mp3')


def save_speech(txt, filename):
    tts =  gTTS(text=txt,lang='zh-TW')
    tts.save('{}.mp3'.format(filename))


def get_noise(thr=25000):
    while True:
        with sr.Microphone() as source:
            buffer = source.stream.read(source.CHUNK)
            energy = audioop.rms(buffer, source.SAMPLE_WIDTH)  # energy of the audio signal
        n = energy
        print(n)
        if n > thr:
            return True


if __name__ == '__main__':
    # save_speech('正在抓取熱門新聞，請稍等','./sounds/crawingnews')
    # save_speech("已經是最大聲了",'./sounds/AlreadyMaxSound')
    # save_speech("已經是最大聲了",'./sounds/AlreadyMinSound')
    # save_speech("好的，已增加音量",'./sounds/IncreaseSound')
    # save_speech("好的，已降低音量",'./sounds/DecreaseSound')
    # save_speech('好的，正在建立串流，請稍等','./sounds/creatingstream')
    print('hi')
