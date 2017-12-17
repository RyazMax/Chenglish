# Chenglish - графическая оболочка
# Автор - Рязанов Максим

from records import* # импорт функций для работы с базами слов
from chsound import* # импорт функций для работы со звуком
from tkinter import* # импорт функций для работы с графическим интерфейсом

def show_help():
    print('Тут мы откроем файл')
def about():
    print('Тут мы откроем файл')

root = Tk()
root.title('СHENGLISH')
root.geometry('1024x620')

menu = Menu(root,title = 'Меню')
root.config(menu = menu)
menu.add_command(label = 'Помощь', command = show_help)
menu.add_command(label = 'О программе',command = about)

lb = Label(root,text = 'Cписок тем')
lb.grid(row = 1,column = 0,columnspan = 2)
ls_b = Listbox(root)
for i in scan():
    ls_b.insert(0,i)
ls_b.grid(row = 2,column = 0, columnspan = 2)


root.mainloop()



