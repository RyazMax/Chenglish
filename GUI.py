# Chenglish - графическая оболочка
# Автор - Рязанов Максим

from records import* # импорт функций для работы с базами слов
from chsound import* # импорт функций для работы со звуком
from tkinter import* # импорт функций для работы с графическим интерфейсом

def warn(label,text,col = 'red'):
    tmp  = label['text']
    label.configure(text = text,fg = col)
    label.after(2000,lambda:label.configure(text = tmp,fg = 'black'))

def addmean(listbox,mean):
    if not mean in listbox.get(0,listbox.size()):
        listbox.insert(0,mean)

FORB_CHAR = '\./:"<>|+%@!?*'
BUTTON_WIDTH = 17
FRAME_WIDTH = 550
FRAME_HEIGHT = 300
class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.root.title('СHENGLISH')
        self.root.geometry('1024x620')

        #self.root.bind('<<Myevent>>',lambda x:print('ok'))

        self.h_menu = Menu(self.root,title = 'Меню')
        self.root.config(menu = self.h_menu)
        self.h_menu.add_command(label = 'Помощь', command = self.show_help)
        self.h_menu.add_command(label = 'О программе',command = self.about)

        self.lb = Label(self.root,text = 'МЕНЮ')
        self.lb.grid(row = 0,column = 0,padx = 10,pady = 15)

        self.thlbl = Label(self.root,text = 'ТЕМЫ')
        self.thlbl.grid(row = 0,column = 2,columnspan = 2)

        self.thlb = Listbox(self.root,height = 19,selectmode = MULTIPLE)
        self.thlb.grid(row = 1,rowspan = 9,column = 2,columnspan = 2)
        #self.root.bind(sequence='<>',func = lambda x:self.thlb.configure(selectmode = MULTIPLE))
        #self.root.bind('<KeyRelease>',func = lambda x:self.thlb.configure(selectmode = SINGLE))

        for i in scan():
            self.thlb.insert(0,i)

        self.cur_frame = 0

    def mainloop(self):
        self.root.mainloop()

    def show_help(self):
        print('Тут мы откроем файл')

    def about(self):
        print('Тут мы откроем файл')

    def creatFrame(self):
        res = Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT,
                    relief=GROOVE, borderwidth=10, )
        res.grid_propagate(False)
        return res

    def setFrame(self, next_frame):
        if self.cur_frame:
            self.cur_frame.grid_forget()
        self.cur_frame = next_frame
        next_frame.grid_propagate(False)
        next_frame.grid(row=1, column=1, rowspan=9, padx=30)

# Показ слов ###################################################################
class ShowWord():
    def __init__(self,root):
        self.frame = root.creatFrame()

        self.but = Button(root.root,text = 'Просмотреть слова',
                    width = BUTTON_WIDTH,
                    command = lambda:root.setFrame(self.frame))
        self.but.grid(row = 1, column = 0,padx = 10)

        self.show_but = Button(self.frame,
                               text = 'Показать',
                               command = lambda:self.show_words(root))
        self.show_but.grid(row = 6, column = 3,columnspan = 2,sticky = 's')

        self.lbl2 = Label(self.frame, text = 'СЛОВА')
        self.lbl2.grid(row = 0,column = 0,columnspan = 3)

        self.wordslb = Listbox(self.frame, width = 65, height = 15)
        self.wordslb.grid(row = 1,column = 0, columnspan = 3,
             rowspan = 6,padx = 15 )

        self.var = IntVar()
        self.var.set(0)

        self.rad0 = Radiobutton(self.frame,text = 'RU',
                                variable = self.var,value = 0)
        self.rad1 = Radiobutton(self.frame,text = 'EN',
                                variable = self.var,value = 1)
        self.rad0.grid(row = 6,column = 3,sticky = 'n')
        self.rad1.grid(row = 6,column = 4,sticky = 'n')

    def show_words(self,root):
        self.wordslb.delete(0, self.wordslb.size())
        themes = [root.thlb.get(i) for i in root.thlb.curselection()]
        if not themes: warn(root.thlbl, 'Выделите тему')
        bor = Bor(get_th(*themes, mode=self.var.get()))
        for rec in bor.get(mode=self.var.get()):
            tmp = ''
            for i in rec.get():
                tmp += i + '; '
            line = str(rec.getk()) + ' - ' + tmp
            self.wordslb.insert(self.wordslb.size()+1, line)

class AddWord():
    def __init__(self,root):
        self.but = Button(root.root, text='Добавить слово',
                             width=BUTTON_WIDTH,
                             command=lambda: root.setFrame(self.frame))
        self.but.grid(row=2, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame, text='Слово на русском:')
        self.lbl1.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2)

        self.lbl2 = Label(self.frame, text='Английский перевод:')
        self.lbl2.grid(row=2, column=0, columnspan=2, pady=10)

        self.ment = Entry(self.frame, width=25)
        self.ment.grid(row=3, column=0, columnspan=2,padx = 50)
        self.ment.bind(sequence='<Return>',
                        func=lambda x: addmean(self.mlb, self.ment.get()))

        self.mbut = Button(self.frame, text='+',
                              command=lambda: addmean(self.mlb, self.ment.get()))
        self.mbut.grid(row=3, column=1,sticky = 'e')

        self.mlb = Listbox(self.frame, width=25)
        self.mlb.grid(row=1, column=3, columnspan=3, rowspan=5,padx = 50)
        self.mlb.bind(sequence='<Delete>',
                         func=lambda x: [self.mlb.delete(i) for i in self.mlb.curselection()])

        self.lbl3 = Label(self.frame, text='Значения')
        self.lbl3.grid(row=0, column=3, columnspan=3)

        self.add_but = Button(self.frame,text = 'Добавить',
                              command = lambda:self.addwords(root),
                              width = BUTTON_WIDTH)
        self.add_but.grid(row = 6,column = 0,columnspan = 2)

        self.fadd_but = Button(self.frame,text = 'Добавить из файла',
                               width = BUTTON_WIDTH)
        self.fadd_but.grid(row = 7,column = 0,columnspan = 2)

    def addwords(self,root):
        if self.ent.get() == '': warn(self.lbl1,'Введите слово')
        elif not self.mlb.size(): warn(self.lbl2,'Введите перевод')
        elif not root.thlb.curselection(): warn(root.thlbl,'Выберите тему')
        else:
            rec  = record(self.ent.get(),*self.mlb.get(0,self.mlb.size()))
            themes = [root.thlb.get(i) for i in root.thlb.curselection()]
            add(rec,rec.getk(),*themes)
            self.add_but['text'] = 'Добавлено'
            self.add_but['fg'] = 'green'
            self.add_but.after(2000,
                func = lambda: self.add_but.configure(text = 'Добавить',fg = 'black'))

class CreateTheme():
    def __init__(self,root):
        self.but = Button(root.root, text='Создать тему',
                          width=BUTTON_WIDTH,
                          command =lambda: root.setFrame(self.frame))
        self.but.grid(row=7, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame,text = 'Название темы')
        self.lbl1.grid(row = 0,column = 0,columnspan = 3,
                       padx = 170,pady = 50)

        self.ent = Entry(self.frame,width = 25)
        self.ent.grid(row = 1,column = 0,columnspan = 2,
                      padx = 170)

        self.crbut = Button(self.frame,width = BUTTON_WIDTH,
                            text = 'Создать',
                            command = lambda: self.create_theme(root))
        self.crbut.grid(row = 5,column = 0,columnspan = 2)


    def create_theme(self,root):
        name = self.ent.get()
        if not name: warn(self.lbl1,'Введите название темы')
        elif not all([not i in name for i in FORB_CHAR]):
            warn(self.lbl1,'Название содержит запрещенные символы')
        else:
            if create_th(self.ent.get()) == 1:
                warn(self.lbl1,'Такая тема уже существует')
            else:
                root.thlb.insert(0,self.ent.get())
                self.ent.delete(0,len(self.ent.get()))

class DeleteTheme():
    def __init__(self,root):
        self.but = Button(root.root, text='Удалить тему',
                          width=BUTTON_WIDTH,
                          command = lambda: root.setFrame(self.frame))
        self.but.grid(row=8, column=0)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame, text='Название темы')
        self.lbl1.grid(row=0, column=0, columnspan=3,
                       padx=170, pady=50)

        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2,
                      padx=170)

        self.delbut = Button(self.frame, width=BUTTON_WIDTH,
                            text='Удалить',
                            command=lambda: self.delete_theme(root))
        self.delbut.grid(row=5, column=0, columnspan=2)

    def delete_theme(self,root):
        selection = root.thlb.curselection()
        if selection:
            for i in reversed(selection):
                del_th(root.thlb.get(i))
                root.thlb.delete(i)
            warn(self.delbut,'Удалено','green')
        else:
            if self.ent.get():
                if not del_th(self.ent.get()):
                    warn(self.lbl1,'Нет такой темы')
                else:
                    warn(self.delbut,'Удалено','green')
                    for i in range(root.thlb.size()):
                        if root.thlb.get(i) == self.ent.get():
                            root.thlb.delete(i)
                            break
                    self.ent.delete(0, len(self.ent.get()))
            else:
                warn(self.lbl1,'Введите название темы'
                               ' или выделите его в списке тем.')

class ChangeWord():
    def __init__(self,root):
        self.but = Button(root.root, text='Изменить слово', width=BUTTON_WIDTH)
        self.but.grid(row=3, column=0, pady=2.5)

class DeleteWord():
    def __init__(self,root):
        self.but = Button(root.root, text='Удалить слово', width=BUTTON_WIDTH)
        self.but.grid(row=4, column=0, pady=2.5)

class TranslWord():
    def __init__(self,root):
        self.but = Button(root.root, text='Перевести слово', width=BUTTON_WIDTH)
        self.but.grid(row=5, column=0, pady=2.5)

class Check():
    def __init__(self,root):
        self.but = Button(root.root, text='Проверка', width=BUTTON_WIDTH)
        self.but.grid(row=6, column=0, pady=2.5)

if __name__ == '__main__':
    window = MainWindow()

    shword = ShowWord(window)
    window.setFrame(shword.frame)
    addword = AddWord(window)
    chword = ChangeWord(window)
    delword = DeleteWord(window)
    trsl = TranslWord(window)
    check = Check(window)
    createth = CreateTheme(window)
    delth = DeleteTheme(window)

    window.mainloop()
"""
# Добавление слова ############################################################


# Изменение слова #########################################################



root.mainloop()
"""


