# Chenglish - графическая оболочка
# Автор - Рязанов Максим

from records import *  # импорт функций для работы с базами слов
from chsound import *  # импорт функций для работы со звуком
from tkinter import *  # импорт функций для работы с графическим интерфейсом
from tkinter import messagebox as mb
from tkinter import filedialog as fd

# MainWindow - главная окно
# Check - область проверки слов
# ShowWord - область вывода слов
# AddWord - область добавления слов
# DeleteWord - область удаления слова
# TranslWord - область перевода слова
# CreateTheme - область создания темы
# DeleteTheme - область удаления темы
# FORB_CHAR - символы запрещенные в названии тем
# BUTTON_WIDTH - ширина кнопки
# FRAME_WIDTH
# FRAME_HEIGHT - размеры области
# MAINCOLOR - цвет фона
# BUTTCOLOR - цвет кнопок на главном окне
# LABCOLOR - цвет надписей на главном окне
# FLAB - стиль надписей

# Изменение надписи на виджете
def warn(label, text, col='red'):
    if not label['fg'] in ['SystemButtonText', 'white']: return
    tmp = label['text']
    tmp2 = label['fg']
    label.configure(text=text, fg=col)
    label.after(2000, lambda: label.configure(text=tmp, fg=tmp2))

# Добавление неповторяющихся элементов в Lisbox
def addmean(listbox, mean, lbl):
    for i in mean:
        if i in LAT[0][:66]:
            warn(lbl, 'Используйте английские буквы')
            return
    if '"' in mean:
        warn(lbl, 'Не используйте "')
        return
    if not mean in listbox.get(0, listbox.size()):
        listbox.insert(0, mean)

# Выделения списка тем
def selthlb(obj, lb):
    if obj.flag:
        lb.select_set(0, END)
        obj.flag = False
    else:
        lb.select_clear(0, END)
        obj.flag = True


FORB_CHAR = '\./:"<>|+%@!?*'
BUTTON_WIDTH = 17
FRAME_WIDTH = 550
FRAME_HEIGHT = 300
MAINCOLOR = '#35BB86'
BUTTCOLOR = '#FFA473'
LABCOLOR = 'white'
FLAB = 'comicsans 14'


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('СHENGLISH')
        self.flag = True
        self.root.configure(bg=MAINCOLOR)

        # self.root.bind('<<Myevent>>',lambda x:print('ok'))

        # self.h_menu = Menu(self.root,title = 'Меню')
        # self.root.config(menu = self.h_menu)
        # self.h_menu.add_command(label = 'Помощь', command = self.show_help)
        # self.h_menu.add_command(label = 'О программе',command = self.about)

        # Надписи
        self.lb = Label(self.root, text='МЕНЮ', bg=MAINCOLOR, fg=LABCOLOR,
                        font=FLAB)
        self.lb.grid(row=0, column=0, padx=10, pady=15)

        self.thlbl = Label(self.root, text='ТЕМЫ', bg=MAINCOLOR, fg=LABCOLOR,
                           font=FLAB)
        self.thlbl.bind('<Button-1>',
                        lambda x: selthlb(self, self.thlb))

        self.thlbl.grid(row=0, column=2, columnspan=2, padx=20)

        self.thlb = Listbox(self.root, height=19, selectmode=MULTIPLE, width=35)
        self.thlb.grid(row=1, rowspan=9, column=2, columnspan=2, padx=10)
        # self.root.bind(sequence='<>',func = lambda x:self.thlb.configure(selectmode = MULTIPLE))
        # self.root.bind('<KeyRelease>',func = lambda x:self.thlb.configure(selectmode = SINGLE))

        for i in scan():
            self.thlb.insert(0, i)

        self.cur_frame = 0 # Текущая область

    def mainloop(self):
        self.root.mainloop()

    def show_help(self):
        print('Тут мы откроем файл')

    def about(self):
        print('Тут мы откроем файл')

    # Создание рабочей области
    def creatFrame(self):
        res = Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT,
                    relief=GROOVE, borderwidth=10, )
        res.grid_propagate(False)
        return res

    # Установка области next_frame в текущую
    def setFrame(self, next_frame):
        if self.cur_frame:
            self.cur_frame.grid_forget()
        self.cur_frame = next_frame
        next_frame.grid_propagate(False)
        next_frame.grid(row=1, column=1, rowspan=9, padx=30)

    # Отображение слов из выделенных тем в Listbox - lb, в режиме var
    def show_words(self, lb, var):
        lb.delete(0, lb.size())
        themes = [self.thlb.get(i) for i in self.thlb.curselection()]
        if not themes: warn(self.thlbl, 'Выделите тему')
        bor = Bor(get_th(*themes, mode=var.get()))
        for rec in bor.get(mode=var.get()):
            tmp = ''
            for i in rec.get():
                tmp += i + '; '
            line = str(rec.getk()) + ' - ' + tmp
            lb.insert(lb.size() + 1, line)


# Показ слов ###################################################################
class ShowWord:
    def __init__(self, root):
        self.frame = root.creatFrame()

        # Кнопки
        self.mbut = Button(root.root, text='Просмотреть слова',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=2, column=0, padx=10)

        self.show_but = Button(self.frame,
                               text='Показать',
                               command=lambda: root.show_words(self.wordslb, self.var))
        self.show_but.grid(row=6, column=3, columnspan=2, sticky='s')

        # Надписи
        self.lbl2 = Label(self.frame, text='СЛОВА')
        self.lbl2.grid(row=0, column=0, columnspan=3)
        # Listbox и кнопки прокрутки
        self.scrollbary = Scrollbar(self.frame)
        self.scrollbary.grid(row=1,column=3)

        self.scrollbarx = Scrollbar(self.frame)

        self.wordslb = Listbox(self.frame, width=65, height=15,
                               yscrollcommand=self.scrollbary.set,
                               xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.wordslb.yview)
        self.scrollbarx.config(command=self.wordslb.xview)
        self.wordslb.grid(row=1, column=0, columnspan=3,
                          rowspan=6, padx=15)
        self.scrollbarx.grid(row=2,column=3)

        # Выбор языка
        self.var = IntVar()
        self.var.set(0)

        self.rad0 = Radiobutton(self.frame, text='RU',
                                variable=self.var, value=0)
        self.rad1 = Radiobutton(self.frame, text='EN',
                                variable=self.var, value=1)
        self.rad0.grid(row=6, column=3, sticky='n')
        self.rad1.grid(row=6, column=4, sticky='n')


class AddWord:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Добавить слово',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=3, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame, text='Слово на русском:')
        self.lbl1.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        # Поле ввода слов
        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2)

        self.lbl2 = Label(self.frame, text='Английский перевод:')
        self.lbl2.grid(row=2, column=0, columnspan=2, pady=10)

        # Поле ввода значений
        self.ment = Entry(self.frame, width=25)
        self.ment.grid(row=3, column=0, columnspan=2, padx=50)
        self.ment.bind(sequence='<Return>',
                       func=lambda x: addmean(self.mlb, self.ment.get(), self.lbl2))

        # Кнопка добавления значений
        self.meanbut = Button(self.frame, text='+',
                              command=lambda: addmean(self.mlb, self.ment.get(), self.lbl2))
        self.meanbut.grid(row=3, column=1, sticky='e')

        # Список текущих добавленных значений
        self.mlb = Listbox(self.frame, width=25)
        self.mlb.grid(row=1, column=3, columnspan=3, rowspan=5, padx=50)
        self.mlb.bind(sequence='<Delete>',
                      func=lambda x: [self.mlb.delete(i) for i in self.mlb.curselection()])

        self.lbl3 = Label(self.frame, text='Значения')
        self.lbl3.grid(row=0, column=3, columnspan=3)

        self.add_but = Button(self.frame, text='Добавить',
                              command=lambda: self.addwords(root),
                              width=BUTTON_WIDTH)
        self.add_but.grid(row=6, column=0, columnspan=2)

        self.fadd_but = Button(self.frame, text='Добавить из файла',
                               width=BUTTON_WIDTH,
                               command=lambda: self.faddwords(root))
        self.fadd_but.grid(row=7, column=0, columnspan=2)

    def faddwords(self, root): # Добавление слов из файла
        if not root.thlb.curselection():
            warn(root.thlbl, 'Выберите тему')
        else:
            file = fd.askopenfilename()
            if file[-4:] != '.txt':
                mb.showwarning('', 'Необходим текствой файл')
            else:
                themes = [root.thlb.get(i) for i in root.thlb.curselection()]
                if addfile(file, *themes):
                    mb.showerror('', 'При добавлении призошла ошибка')
                else:
                    mb.showinfo('', 'Слова успешно добавлены')

    def addwords(self, root): # Добавление слов
        word = self.ent.get()
        if word == '':
            warn(self.lbl1, 'Введите слово')
        elif not self.mlb.size():
            warn(self.lbl2, 'Введите перевод')
        elif not root.thlb.curselection():
            warn(root.thlbl, 'Выберите тему')
        else:
            for i in word:
                if i in LAT[1][:52]:
                    warn(self.lbl1, 'Используйте русские буквы')
                    return
            if '"' in word:
                warn(self.lbl1, 'Нельзя использовать "')
                return
            rec = record(word, *self.mlb.get(0, self.mlb.size()))
            themes = [root.thlb.get(i) for i in root.thlb.curselection()]
            add(rec, rec.getk(), *themes)
            self.ent.delete(0, END)
            self.ment.delete(0, END)
            self.mlb.delete(0, END)
            self.add_but['text'] = 'Добавлено'
            self.add_but['fg'] = 'green'
            self.add_but.after(2000,
                               func=lambda: self.add_but.configure(text='Добавить', fg='black'))


class CreateTheme:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Создать тему',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=8, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame, text='Название темы')
        self.lbl1.grid(row=0, column=0, columnspan=3,
                       padx=170, pady=50)

        # Поле ввода названия темы
        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2,
                      padx=170)

        self.crbut = Button(self.frame, width=BUTTON_WIDTH,
                            text='Создать',
                            command=lambda: self.create_theme(root))
        self.crbut.grid(row=5, column=0, columnspan=2)

    def create_theme(self, root): # Cоздание темы
        name = self.ent.get()
        if not name:
            warn(self.lbl1, 'Введите название темы')
        elif not all([not i in name for i in FORB_CHAR]):
            warn(self.lbl1, 'Название содержит запрещенные символы')
        else:
            if create_th(self.ent.get()) == 1:
                warn(self.lbl1, 'Такая тема уже существует')
            else:
                root.thlb.insert(0, self.ent.get())
                self.ent.delete(0, END)
                warn(self.crbut, 'Тема создана', 'green')


class DeleteTheme:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Удалить тему',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=9, column=0)

        self.frame = root.creatFrame()

        self.lbl1 = Label(self.frame, text='Название темы')
        self.lbl1.grid(row=0, column=0, columnspan=3,
                       padx=170, pady=50)
        # Поле ввода названия темы
        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2,
                      padx=170)

        self.delbut = Button(self.frame, width=BUTTON_WIDTH,
                             text='Удалить',
                             command=lambda: self.delete_theme(root))
        self.delbut.grid(row=5, column=0, columnspan=2)

    def delete_theme(self, root): # Удаление темы
        selection = root.thlb.curselection()
        if selection:
            for i in reversed(selection):
                del_th(root.thlb.get(i))
                root.thlb.delete(i)
            warn(self.delbut, 'Удалено', 'green')
            self.ent.delete(0, END)
        else:
            if self.ent.get():
                if not del_th(self.ent.get()):
                    warn(self.lbl1, 'Нет такой темы')
                else:
                    warn(self.delbut, 'Удалено', 'green')
                    for i in range(root.thlb.size()):
                        if root.thlb.get(i) == self.ent.get():
                            root.thlb.delete(i)
                            break
                    self.ent.delete(0, len(self.ent.get()))
            else:
                warn(self.lbl1, 'Введите название темы'
                                ' или выделите его в списке тем.')


class ChangeWord: # УЧАСТОК КОТОРЫЙ БУДЕТ ПОТОМ
    def __init__(self, root):
        self.mbut = Button(root.root, text='Изменить слово',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame))
        self.mbut.grid(row=4, column=0, pady=2.5)

        self.frame = root.creatFrame()
        self.frame2 = root.creatFrame()

        # Надписи на 1-ом фрейме
        self.lbl = [None] * 7
        self.lbl[0] = Label(self.frame, text='Выбрать слово')
        self.lbl[0].grid(row=0, column=0, columnspan=2, pady=10)
        self.lbl[1] = Label(self.frame, text='Новое слово')
        self.lbl[1].grid(row=3, column=0, columnspan=2, sticky='s')
        self.lbl[2] = Label(self.frame, text='СЛОВА')
        self.lbl[2].grid(row=0, column=5, columnspan=2)
        # На 2-ом
        self.lbl[3] = Label(self.frame2, text='Значение')
        self.lbl[3].grid(row=0, column=0, columnspan=2, pady=10)
        self.lbl[4] = Label(self.frame2, text='Новое значение')
        self.lbl[4].grid(row=3, column=0, columnspan=2, sticky='s')
        self.lbl[5] = Label(self.frame2, text='Значения')
        self.lbl[5].grid(row=0, column=3, columnspan=2)
        self.lbl[6] = Label(self.frame2, text='Изменения')
        self.lbl[6].grid(row=0, column=5, columnspan=2)

        # Поля ввода на 1-ом фрейме
        self.ent = [None] * 4
        self.ent[0] = Entry(self.frame, width=30)
        self.ent[0].grid(row=1, column=0, columnspan=2, padx=15)
        self.ent[1] = Entry(self.frame, width=30)
        self.ent[1].grid(row=4, column=0, columnspan=2)
        # На 2-ом
        self.ent[2] = Entry(self.frame2, width=30)
        self.ent[2].grid(row=1, column=0, columnspan=2, padx=8)
        self.ent[3] = Entry(self.frame2, width=30)
        self.ent[3].grid(row=4, column=0, columnspan=2)

        # Кнопки на 1-ом фрейме
        self.but = [None] * 6
        self.but[0] = Button(self.frame, bg='#777777')
        self.but[0].grid(row=1, column=2)
        self.but[1] = Button(self.frame, width=BUTTON_WIDTH,
                             text='Далее',
                             command=lambda: self.nextFrame(root))
        self.but[1].grid(row=6, column=0, columnspan=2)
        self.but[2] = Button(self.frame, width=BUTTON_WIDTH,
                             text='Показать',
                             command=lambda: root.show_words(self.lb[0], self.var))
        self.but[2].grid(row=6, column=5, columnspan=2)
        # На 2-ом
        self.but[3] = Button(self.frame2, bg='#777777')
        self.but[3].grid(row=1, column=2)
        self.but[4] = Button(self.frame2, text='+')
        self.but[4].grid(row=4, column=2)
        self.but[5] = Button(self.frame2, text='Изменить',
                             width=BUTTON_WIDTH)
        self.but[5].grid(row=5, column=4, columnspan=2, pady=15)

        # Listbox на 1-ом фрейме
        self.lb = [None] * 3
        self.lb[0] = Listbox(self.frame, width=40)
        self.lb[0].grid(row=1, column=5, rowspan=4, columnspan=2, padx=30)
        # На 2-ом
        self.lb[1] = Listbox(self.frame2, width=23)
        self.lb[1].grid(row=1, column=3, rowspan=4, columnspan=2, padx=5)
        self.lb[2] = Listbox(self.frame2, width=23)
        self.lb[2].grid(row=1, column=5, rowspan=4, columnspan=2, padx=5)

        # Кнопки выбора языка на 1-ом фреме
        self.var = IntVar(value=0)
        self.rbut = [None] * 2
        self.rbut[0] = Radiobutton(self.frame, text='RU', variable=self.var, value=0)
        self.rbut[1] = Radiobutton(self.frame, text='EN', variable=self.var, value=1)
        for i in range(2): self.rbut[i].grid(row=5, column=5 + i)

    def nextFrame(self, root):
        tmp = self.ent[0].get()
        if not tmp:
            warn(self.lbl[0], 'Выберите слово')
            return

        root.setFrame(self.frame2)


class ChangeTheme: # УЧАСТОК КОТОРЫЙ БУДЕТ ПОТОМ
    def __init__(self, root):
        self.mbut = Button(root.root, text='Переместить слово',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame))
        self.mbut.grid(row=5, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lbl = [None] * 2
        self.lbl[0] = Label(self.frame, text='СЛОВА')
        self.lbl[0].grid(row=0, column=0, columnspan=2, pady=10)
        self.lbl[1] = Label(self.frame, text='ТЕМЫ')
        self.lbl[1].grid(row=0, column=3, columnspan=2)

        self.lb = [None] * 2
        self.lb[0] = Listbox(self.frame, width=40)
        self.lb[0].grid(row=1, column=0, rowspan=5, columnspan=2, padx=10)
        self.lb[1] = Listbox(self.frame, width=40)
        self.lb[1].grid(row=1, column=3, rowspan=5, columnspan=2, padx=10)

        self.var = IntVar(value=0)
        self.rbut = [None] * 2
        self.rbut[0] = Radiobutton(self.frame, text='RU', variable=self.var, value=0)
        self.rbut[1] = Radiobutton(self.frame, text='EN', variable=self.var, value=1)
        for i in range(2): self.rbut[i].grid(row=6, column=0 + i)

        self.but = [None] * 2
        self.but[0] = Button(self.frame, width=BUTTON_WIDTH,
                             text='Переместить')
        self.but[0].grid(row=7, column=3, columnspan=2)
        self.but[1] = Button(self.frame, width=BUTTON_WIDTH,
                             text='Показать',
                             command=lambda: root.show_words(self.lb[0], self.var))
        self.but[1].grid(row=7, column=0, columnspan=2)

        self.chvar = IntVar(value=0)
        self.chbut = Checkbutton(self.frame, text='Удалить',
                                 variable=self.chvar)
        self.chbut.grid(row=6, column=3, columnspan=2)


class DeleteWord:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Удалить слово',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=4, column=0, pady=2.5)

        self.frame = root.creatFrame()
        self.flag = False

        self.lbl1 = Label(self.frame, text='Выбрать слово')
        self.lbl1.grid(row=0, column=0, columnspan=2)

        # Поле ввода слова
        self.ent = Entry(self.frame, width=25)
        self.ent.grid(row=1, column=0, columnspan=2,padx=10)

        # Кнопка для поиска слова в списке
        self.chbut = Button(self.frame, bg='#777777',
                            command=self.showmean)
        self.chbut.grid(row=1, column=2)

        # Выбор языка
        self.v1 = IntVar()
        self.v1.set(0)

        self.r1 = Radiobutton(self.frame, text='RU',
                              variable=self.v1, value=0)
        self.r2 = Radiobutton(self.frame, text='EN',
                              variable=self.v1, value=1)
        self.r1.grid(row=3, column=0)
        self.r2.grid(row=3, column=1)

        self.themes = []

        # Кнопка вывода на слов в Listbox
        self.showbut = Button(self.frame, text='Показать',
                              width=BUTTON_WIDTH,
                              command=lambda: self.themes.append(root.thlb.curselection())
                              if not root.show_words(self.lb[0], self.v1) else 0)
        self.showbut.grid(row=4, column=0, columnspan=2)

        # Кнопка удаления
        self.delbut = Button(self.frame, text='Удалить',
                             width=BUTTON_WIDTH,
                             command=lambda: self.delete(root))
        self.delbut.grid(row=6, column=0, columnspan=2)

        self.lbl2 = Label(self.frame, text='Слова')
        self.lbl2.grid(row=0, column=4, columnspan=2, pady=10)
        self.lbl3 = Label(self.frame, text='Значения')
        self.lbl3.grid(row=0, column=6, columnspan=2, pady=10)
        self.lbl3.bind('<Button-1>', lambda x: selthlb(self, self.lb[1]))

        # Listbox[0]- для слов Listbox[1] - для значений
        # sroll - соответствующие кнопки прокрутки
        self.lb = [None, None]
        self.scroll = [None, None]
        for i in range(2):
            self.scroll[i] = Scrollbar(self.frame)
            self.lb[i] = Listbox(self.frame, width=25, height=13,
                            yscrollcommand = self.scroll[i].set)
            self.lb[i].grid(row=1, column=4 + i * 2, columnspan=2, rowspan=9,
                            padx=5)
            self.scroll[i].config(command=self.lb[i].yview)
        self.lb[1].config(selectmode=MULTIPLE)
        for i in range(2):
            self.scroll[i].grid(row=1+i,column=3)

    def showmean(self): # Выделение введенного слова и вывод его значений
        word = self.ent.get().strip()
        if self.lb[0].size() < 1:
            warn(self.lbl1, 'Выведите слова из тем')
            return
        if word:
            for i in range(self.lb[0].size()):
                if word == self.lb[0].get(i).split('-')[0].strip():
                    self.lb[0].selection_clear(0, END)
                    self.lb[0].selection_set(i)
                    break
            else:
                warn(self.lbl1, 'Слова нет в списке')
                return
        selection = self.lb[0].curselection()
        if selection:
            word = self.lb[0].get(selection)
            word, mean = word.split('-')
            mean = mean.split(';')[:-1]
            self.ent.delete(0, END)
            self.ent.insert(0, word)
            self.lb[1].delete(0, END)
            for i in mean:
                self.lb[1].insert(0, i)
        else:
            warn(self.lbl1, 'Введите или выделите слово')

    def delete(self, root): # Удаление слова с выделенными значениями
        selection = self.lb[1].curselection()
        word = self.ent.get().strip()
        if selection:
            if word:
                value = set(self.lb[1].get(i).strip() for i in selection)
                themes = [root.thlb.get(i) for i in self.themes[0]]
                if del_rec(word, value, *themes):
                    warn(self.lbl1, 'Удаление прошло успешно', 'green')
                    self.ent.delete(0, END)
                    for i in reversed(selection): self.lb[1].delete(i)
                    for i in range(self.lb[0].size()):
                        if word == self.lb[0].get(i).split('-')[0].strip():
                            self.lb[0].delete(i)
                            tmp = ''
                            for j in range(self.lb[1].size()):
                                tmp += self.lb[1].get(j) + '; '
                            if tmp:
                                self.lb[0].insert(i, word + ' - ' + tmp)
                            break
                else:
                    warn(self.lbl1, 'Слово не было найдено')
            else:
                warn(self.lbl1, 'Выберите слово')
        else:
            warn(self.lbl1, 'Выберите значение')


class TranslWord:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Перевести слово',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=5, column=0, pady=2.5)

        self.frame = root.creatFrame()

        self.lb = Listbox(self.frame, width=45)
        self.lb.grid(row=1, rowspan=8, column=3, columnspan=3,
                     padx=30)

        self.lbl = Label(self.frame, text='Перевод')
        self.lbl.grid(row=0, column=3, columnspan=3,
                      pady=15, padx=30)

        self.lbl2 = Label(self.frame, text='Слово для перевода')
        self.lbl2.grid(row=2, column=0, columnspan=2)

        self.ent = Entry(self.frame, width=30)
        self.ent.grid(row=3, column=0, columnspan=2, padx=15)

        self.trbut = Button(self.frame, text='Перевести',
                            width=BUTTON_WIDTH,
                            command=self.trword)
        self.trbut.grid(row=4, column=0, columnspan=2)

        self.sbut = Button(self.frame, text='Произнести',
                           width=BUTTON_WIDTH,
                           command=lambda: self.sound())
        self.sbut.grid(row=5, column=0, columnspan=2)

    def sound(self):
        word = self.ent.get()
        if '"' in word:
            warn(self.lbl2, 'Нельзя использовать "')
        for i in word:
            if i in LAT[0][:66]:
                warn(self.sbut, 'Только английские')
                return
        playword(word)

    def trword(self, mode=0): # Перевод слова
        word = self.ent.get()
        if '"' in word:
            warn(self.lbl2, 'Нельзя использовать "')
        if not word:
            warn(self.lbl2, 'Введите слово')
            return
        self.lb.delete(0, END)
        if mode:
            self.lb.insert(0, 'Перевод из интернета')
        else:
            meanings = transl(word)
            if meanings:
                for i in meanings:
                    self.lb.insert(0, i)
            else:
                self.lb.insert(0, 'Слово не найдено')


class Check:
    def __init__(self, root):
        self.mbut = Button(root.root, text='Проверка',
                           width=BUTTON_WIDTH,
                           command=lambda: root.setFrame(self.frame),
                           bg=BUTTCOLOR,
                           fg=LABCOLOR)
        self.mbut.grid(row=1, column=0, pady=2.5)
        self.frame = root.creatFrame()
        self.frame2 = root.creatFrame()

        self.mode = 0 # Режим проверки
        self.answered = False # Был ли дан ответ на вопрос
        self.cnt = 0 # оставшееся количество вопросов
        self.corr = 0 # количество правильных ответов

        # Надписи на главном окне проверки
        self.lbl = [None] * 6
        self.lbl[0] = Label(self.frame, text='Режим')
        self.lbl[0].grid(row=0, column=0, columnspan=2, pady=15)
        self.lbl[1] = Label(self.frame, text='Доп. опции')
        self.lbl[1].grid(row=0, column=3, columnspan=3)
        self.lbl[2] = Label(self.frame, text='Язык')
        self.lbl[2].grid(row=2, column=3, columnspan=3, sticky='s')
        # Надписи на окне во время проверки
        self.lbl[3] = Label(self.frame2, text='Слово')
        self.lbl[4] = Label(self.frame2, text='Возможные переводы')
        self.lbl[5] = Label(self.frame2, text='Правильно/Неправильно')

        # Поле ввода ответа
        self.ent = Entry(self.frame2, width=30)
        self.ent.bind('<Return>', lambda x: self.next(root))

        # Кнопки на главном окне проверки
        self.but = [None] * 8
        self.but[0] = Button(self.frame, text='Экзамен',
                             width=BUTTON_WIDTH,
                             command=lambda: self.questions(root, 1))
        self.but[0].grid(row=1, column=0, columnspan=2, pady=15, padx=30)
        self.but[1] = Button(self.frame, text='Обычный',
                             width=BUTTON_WIDTH,
                             command=lambda: self.questions(root, 2))
        self.but[1].grid(row=2, column=0, columnspan=2, pady=15)
        self.but[2] = Button(self.frame, text='Помню-не помню',
                             width=BUTTON_WIDTH,
                             command=lambda: self.questions(root, 3))
        # self.but[2].grid(row=3,column=0,columnspan=2,pady=15)

        # Кнопки на окне проверки
        self.but[3] = Button(self.frame2, text='Помню',
                             width=BUTTON_WIDTH)
        self.but[4] = Button(self.frame2, text='Не помню',
                             width=BUTTON_WIDTH)
        self.but[5] = Button(self.frame2, text='Выйти',
                             command=lambda: self.end_check(root))
        self.but[6] = Button(self.frame2, text='Повторить',
                             width=BUTTON_WIDTH,
                             command=lambda: playword(self.ask.ask()))
        self.but[7] = Button(self.frame2, text='Ответить',
                             width=BUTTON_WIDTH,
                             command=lambda: self.next(root))
        # Варианты
        self.lb = Listbox(self.frame2)
        self.lb.grid(row=2, rowspan=5, column=4, columnspan=2)
        # Аудирование
        self.voice_var = IntVar(value=0)
        self.voice = Checkbutton(self.frame, text='Аудирование',
                                 variable=self.voice_var)
        self.voice.grid(row=1, column=3, columnspan=3, padx=50)
        # Выбор языка
        self.lan_var = IntVar(value=0)
        self.rad = [None] * 2
        for i, j in enumerate(['RU-EN', 'EN-RU']):
            self.rad[i] = Radiobutton(self.frame, text=j,
                                      variable=self.lan_var, value=i)
            self.rad[i].grid(row=3, column=3 + i * 2)

    def questions(self, root, mode): # Включение проверки

        # Проверка на корректность режимов
        if not root.thlb.curselection():
            warn(root.thlbl, 'Выберите тему')
            return

        lan = self.lan_var.get() # Выбранный язык
        themes = [root.thlb.get(i) for i in root.thlb.curselection()] # Темы
        sound = self.voice_var.get() # Включено ли аудирование
        if sound and not lan:
            warn(self.lbl[1], 'Только в английском')
            return

        self.ask = Ask_question(*themes, mode=lan)
        self.cnt = len(self.ask.base)
        if self.cnt < 1:
            warn(root.thlbl, 'В теме не слов')
            del (self.ask)
            return

        # Обнуление данных, удаление лишних виджетов
        self.answered = False
        self.lb.delete(0, END)
        self.mode = mode
        self.but[7]['text'] = 'Ответить'
        self.corr = 0

        for i in range(3, 8):
            self.but[i].grid_forget()
        self.ent.grid_forget()
        for i in range(3, 6):
            self.lbl[i].grid_forget()
        self.lbl[4].grid(row=1, column=4, columnspan=2)

        word = self.ask.ask()
        root.setFrame(self.frame2)
        self.lbl[5]['text'] = ''
        self.but[5].grid(row=0, column=0)

        # Размещение необходимых виджетов
        if mode in [1, 2]:

            self.ent.grid(row=4, column=2, columnspan=2, padx=60)
            self.lbl[5].grid(row=2, column=2, columnspan=2)
            self.but[7].grid(row=5, column=2, columnspan=2)
            if sound:
                # root.setFrame(self.frame2)
                self.but[6].grid(row=3, column=2, pady=60, columnspan=2)
                self.frame.after(50, lambda: playword(word))
            else:
                self.lbl[3].grid(row=3, column=2, pady=60, columnspan=2)
                self.lbl[3]['text'] = word
                self.lbl[3]['font'] = 30
            root.setFrame(self.frame2)

    def next(self, root): # Переход к след. вопросу

        sound = self.voice_var.get()
        if self.answered: # Уже был дан ответ, перейти к следующему вопросу
            self.lbl[5]['text'] = ''
            self.answered = False
            word = self.ask.ask()
            if self.mode == 1 and self.cnt < 1:# Ответили на все вопросы в экзамене
                self.end_check(root)
                return

            self.lbl[3]['text'] = word
            self.but[7]['text'] = 'Ответить'
            self.ent.delete(0, END)
            self.lb.delete(0, END)
            if sound:
                self.frame.after(50, lambda: playword(word))
            return
        # Не было ответа на вопрос, проверить его
        if self.mode in [1, 2]:
            g, value = self.ask.check(self.ent.get())
        if g:
            self.lbl[5].configure(text='Правильно', fg='green', font=30)
            self.corr += 1
        else:
            self.lbl[5].configure(text='Неправильно', fg='red', font=30)
        for i in self.ask.secret.get():
            self.lb.insert(0, i)
        self.but[7]['text'] = 'Дальше'
        self.answered = True
        self.cnt -= 1

    def end_check(self, root): # Завершение проверки
        if self.mode == 1:
            mb.showinfo('', 'Вы правильно ответили на: ' + str(self.corr)
                        + ' вопросов из ' + str(len(self.ask.base)))
        root.setFrame(self.frame)


if __name__ == '__main__':
    initdir()
    window = MainWindow()
    check = Check(window)
    shword = ShowWord(window)
    window.setFrame(check.frame)
    addword = AddWord(window)
    # chword = ChangeWord(window)
    # chth = ChangeTheme(window)
    delword = DeleteWord(window)
    trsl = TranslWord(window)
    createth = CreateTheme(window)
    delth = DeleteTheme(window)
    window.mainloop()
