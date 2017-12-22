#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import os
from os import path
import speech_recognition as sr
from gtts import gTTS

def rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Say something!')
        audio = r.listen(source)

    try:
        sttTXT_org = r.recognize_google(audio, language = 'zh-TW')
        print("Google Speech Recognition thinks you said: " + sttTXT_org)
        return sttTXT_org
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return 0
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
        return 0

def t2speech(txt):
    tts =  gTTS(text=txt,lang='zh-TW')
    tts.save('temp.mp3')
    os.system('mpv temp.mp3')
    os.remove('temp.mp3')

#t2speech("忠孝東路走九遍")
