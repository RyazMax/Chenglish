# Модуль с командами для работы с базой слов
# Рязанов Максим
########################################################################
# LANG - текущий языковой режим
# SHEBANG - подпись
# EXT - расширение файлов тем
# scan(name = EXT) - поиск файлов, name - формат файла
# open_th(name) - открытие темы, name - название темы
# del_th(name) - удаление темы, name - название темы
# save(name,obj) - сохранение obj в файл - name
# add(rec,key,theme) - добавление слова rec в список тем theme по ключу key
# addfile(file,theme) - добавление слов из файла в темы
# del_rec(key,theme,mode = 'all') - удаление слова key из темы в режиме mode
# change(rec,key,new_key = key,mode = 'all') - изменение слова key в rec в
#                                                   в режиме mode
# change_th(key,th1,th2) - перемещение слова key из темы 1 в тему 2
# transl (key, show_theme = False) - возврат перевода слова key(cписок значений)

import os
import pickle as pcl
from random import randint

LANGD = './RUS-ENG/'
LANG = ['en','ru']
EXT = '.cheng'
LAT = ['','']
LAT[1] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LAT[1] += LAT[1].lower()+' '
LAT[0] = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
LAT[0] += LAT[0].lower()+' '
SHEBANG = b'CHENG0:52'


##############################################################################
class record:
    def __init__(self,lan1,*lan2):
        self._word = lan1
        self._lan2 = set(lan2)

    def __repr__(self):
        return (str(self.get()))

    def chname(self, new_name):
        self._word = new_name

    def append(self,rec):
        self._lan2.update(rec.get())

    def getk(self):
        return self._word

    def get(self):
        return self._lan2
    
    def remove(self,*lname):
        for name in lname:
            if name in self._lan2:
                self._lan2.remove(name)

class Ask_question:
    def __init__(self,*ltheme,mode = 0):
        print(ltheme)
        self.base = get_th(*ltheme,mode = mode)
        self.mode = mode
        if type(self.base) == int: self.secret = self.base
        else: self.secret = 0

    def ask(self):
        if self.secret: return self.secret
        keys = list(self.base.keys())
        self.secret = self.base[keys[randint(0,len(keys)-1)]]
        return self.secret.getk()

    def check(self,value):
        if type(self.secret) == int: return self.secret
        if value in self.secret.get():
            self.secret = 0
            return True,{value}
        else:
            value = self.secret.get()
            self.secret = 0
            return False,value

class Vertex:
    def __init__(self,rec = 0):
        self.next = {}
        self.leaf = True if rec else False
        self.rec = rec

class Bor:
    def add(self,rec):
        v = 0
        for i in rec.getk():
            if not self.vs[v].next.get(i):
                self.vs.append(Vertex())
                self.vs[v].next[i] = self.sz
                self.sz += 1
            v = self.vs[v].next[i]
        if self.vs[v].leaf:
            self.vs[v].append(rec)
        else:
            self.vs[v].leaf = True
            self.vs[v].rec = rec

    def __init__(self,recs):
        recs = recs.values()
        self.vs = [Vertex(0)]
        self.sz = 1
        for i in recs:
            self.add(i)

    def get(self,v = 0,mode = 0):
        res = []
        if self.vs[v].leaf:
            res.append(self.vs[v].rec)
        for i in LAT[mode]:
            if self.vs[v].next.get(i):
                res += self.get(self.vs[v].next[i],mode)
        return res

def scan(name = EXT,): 
    return [i[:-len(name)] 
            for i in os.listdir(LANGD) if i[-len(name):] == name]

def create_th(name):
    lbase = scan()
    if not name in lbase:
        file = open(LANGD+name+EXT,'wb')
        file.write(SHEBANG)
        pcl.dump([{},{}],file)
        file.close()
        return ([{},{}])
    else:
        return 1

def open_th(name):
    lbase = scan()
    if name in lbase:
        file = open(LANGD+name+EXT,'br')
        shebang = file.read(len(SHEBANG))
        if shebang == SHEBANG:
            res = pcl.load(file)
            file.close()
            return(res)
        else:
            file.close()
            return 2
    else:
        return 1

def del_th(*lname):
    lbase = scan()
    g = 0
    for name in lname:
        if name in lbase:
            os.remove(LANGD+name+EXT)
            g += 1
    return g

def save(name,obj):
    lbase = scan()
    if name in lbase:
        file = open(LANGD+name+EXT,'bw')
        file.write(SHEBANG)
        pcl.dump(obj,file)
        file.close()
        return 0
    else:
        return 1


def add(rec,key,*ltheme):
    lbase = scan()
    g = 0
    b = False
    cur_base = 0
    i = None
    print(ltheme)
    for i in ltheme:
        if i in lbase:
            cur_base = open_th(i)
            if type(cur_base) == int: return cur_base,1
            # Добавление в русский словарь
            if cur_base[0].get(key):
                cur_base[0][key].append(rec)
            else:
                cur_base[0][key] = rec # Возможно неправильное сложения объекта record
            # Добавление в английский словарь
            for j in rec.get(): # Посмотреть переход по сету
                if cur_base[1].get(j):
                    cur_base[1][j].append(record(j,key))
                else:
                    cur_base[1][j] = record(j,key)
            g += 1
        b |= save(i,cur_base)
    return g,b
    


def addfile(file,*ltheme):
    file  = open(file+'.txt','r')
    for i in file:
        if not '-' in i: return 1
        key,*word = i.split('-')
        if not ',' in word: return 1
        word = set(word.split(','))
        add(record(key,word),key,ltheme)
    file.close()
    return 0

def del_rec(key,value,*theme,mode = 'all'):
    g = 0
    for i in theme:
        cur_base = open_th(i)
        if type(cur_base) == int:
            g += 1
            continue
        if cur_base[0].get(key): lan = 0
        else: lan = 1
        if not cur_base[lan].get(key): # Нет такого ключа
            g += 1
            continue
        if mode == 'all':
            value = cur_base[lan][key].get()
            del(cur_base[lan][key])
        else:
            for j in value:
                cur_base[lan][key].remove(j)
                if len(cur_base[lan][key].get()) == 0:
                    del(cur_base[lan][key])
        for j in value:
            if cur_base[lan^1].get(j):
                cur_base[lan^1][j].remove(key)
                if len(cur_base[lan^1][j].get()) == 0:
                    del(cur_base[lan^1][j])
        save(i,cur_base)
    return g

def change(mean,new_mean,key,new_key = 0,*theme):
    g = 0
    #if new_key == 0: new_key = key
    def rchanging(mean,new_mean,key,new_key,mode = 0):# Рекурсивное удаление
        if cur_base[0].get(key): lan = 0
        else: lan = 1
        if not cur_base[lan].get(key): # Нет такого ключа
            return
        rec = cur_base[lan][key]
        if mode:
            rec = record(key,*mean)

        # Изменение ключа key на new_key
        if new_key:
            # Если будут удаляться существуюшие значения при одинаковых заменах значениЙ смотри сюда
            if not mode:
                del (cur_base[lan][key])
            else:
                cur_base[lan][key].remove(*mean)
                if len(cur_base[lan][key].get()) < 1:
                    del (cur_base[lan][key])

            rec.chname(new_key)
            if cur_base[lan].get(new_key):
                cur_base[lan][new_key].append(rec)
            else:
                cur_base[lan][new_key] = rec

            if mode: return # Удалить изменить только ключ, без замены значений

            for j in rec.get():
                rchanging([key],[new_key],j,0)
        else:
            new_key = key
        # Изменение значений
        for j in range(len(mean)):
            cur_base[lan][new_key].remove(mean[j])
            cur_base[lan][new_key].append(record(new_key,*[new_mean[j]]))
            rchanging([new_key],[new_key],mean[j],new_mean[j],1)

    for i in theme:  # Проход по темам
        cur_base = open_th(i)
        if type(cur_base) == int:
            g += 1
            continue
        rchanging(mean,new_mean,key,new_key)
        save(i,cur_base)

    return g

def change_th(key,th1,th2,mode = 0):
    cur_base = open_th(th1)
    if type(cur_base) == 'int': return cur_base
    if cur_base[0].get(key):
        add(cur_base[0][key],key,th2)
        if mode:
            del_rec(key,th1,mode = 'point')
        return 0
    if cur_base[1].get(key):
        for i in cur_base[1][key].getk():
            add(record(i,key),i,th2)
        if mode:
            del_rec(key,set(),th1, mode = 'all') # Подумать на способом удаления записей по английскому ключу
        return 0
    return 3 # Нет такого ключа

# Получение словаря всех слов в темах theme
def get_th(*theme,mode = 0):
    res = {}
    #print(theme)
    for i in theme:
        cur_base = open_th(i)
        if type(cur_base)== int: return cur_base
        #print(cur_base)
        for j in cur_base[mode].keys():
            if res.get(j):
                res[j].append(cur_base[mode][j])
            else:
                res[j] = cur_base[mode][j]
    return res

def transl(key, show_theme = False):
    lbase = scan()
    res = set()
    for i in lbase:
        cur_base = open_th(i)
        if type(cur_base) == int: return cur_base
        if cur_base[0].get(key):
            res.update(cur_base[0][key].get())
        if cur_base[1].get(key):
            res.update(cur_base[1][key].get())
    if len(res) == 0: return 0
    return list(res)

if __name__ == '__main__':
   pass