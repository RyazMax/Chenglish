import pygame.mixer as mxr
from gtts import gTTS
import os

def chconect():
    try:
        tmp = gTTS('a')
        tmp.save('tmp.mp3')
        return True
    except:
        return False
    
def init_sound():
    mxr.init()
    if not ('tmp.mp3' in os.listdir() and 'tmp2.mp3' in os.listdir()):
        if chconect():
            os.replace('tmp.mp3','tmp2.mp3')
        else:
            print('Нет подключения')
            
def make_word(word,lg = 'en'):
    try:
        a = gTTS(word,lang = lg)
        a.save('tmp.mp3')
        return 0
    except:
        return 1

def play_word():
    try:
        mxr.music.load('tmp.mp3')
        mxr.music.play()
        return 0
    except:
        return 1

def del_word():
    mxr.music.load('tmp2.mp3')
