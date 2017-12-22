
import os

# Функция воспроизведения слово с помощью встроенного диктора Windows
def playword(word):
    file = open('sound.vbs','w')
    tmp = 'Set sapi=CreateObject("sapi.spvoice")\n'
    file.write(tmp)
    file.write('sapi.Speak"'+(word)+'"')
    file.close()
    os.system('sound.vbs')