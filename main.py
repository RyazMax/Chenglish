# Chenglish - проверка знаний по английскому языку

# Автор: Рязанов Максим
from console import *
from records import *
from chsound import *

print('=' * 30, 'СHENGLISH', '=' * 30, '\n')

while (True):
    print_menu()
    cmd = read_cmd()
    print(cmd)
    if cmd == [0]:
        break

    if cmd == [1]:
        print('ТЕМЫ:')
        for i,j in enumerate(scan()):
            print(i,j)
        cmd = read_cmd('Введите номер темы:', 'Темы с таким номером не существует')
        if cmd == -1: continue
        if cmd == []: theme  = scan()
        else:
            theme = [scan()[i] for i in cmd]
        print(cmd)
        print('0. - сортировать по русским словам')
        print('1. - cортировать по английским словам')

        cmd = read_cmd('Введите номер режима','Неверный режим')
        if cmd != [0] and cmd != [1]:
            print('Неверный режим!')
            continue
        elif cmd == -1: continue

        bor = Bor(get_th(*theme,mode = cmd[0]))
        for i in bor.get(mode = cmd[0]):
            print(i.getk(), ' \t - \t',i.get())
        input('Для продолжения нажмите Enter...')
        continue

    if cmd == [2]:
        # Вывести варинты тестирования
        cmd = read_cmd()
        # Тестирование

        input('Для продолжения нажмите Enter...')
        continue

    if cmd == [3]:
        word1 = input('Введите слово/фразу на русском\n')
        word2 = input('Введите слово/фразу на английском(разделяйте фразы ";"\n')
        word2 = word2.split(';')

        theme = input('Введите название темы в которую будут'
                      ' добавлены слова (разделяйте ";"):').split(';')
        print(theme)
        if add(record(word1,*word2),word1,*theme)[1]:
            print('Нет такой темы!')
        else:
            print('Cлова добавлены!')
        input('Для продолжения нажмите Enter...')
        continue

    if cmd == [4]:
        word = input('Введите слово для удаления:\n')
        meanings = input('Введите значения для удаления(разделяя ;)'
                         '\n(пустая строка для удаления всех значений слова')
        meanings = meanings.split(';')
        print('Темы:')
        for i in scan():
            print(i)
        theme = input('Введите названия тем(разделяя ;),пустая для всех').split(';')
        if theme == ['']: theme = scan()
        if meanings == ['']:
            del_rec(word,meanings,*theme,mode = 'all')
        else:
            del_rec(word,meanings,*theme,mode = 'point')
        print('Удалено')



    if cmd == [5]:
        word = input('Введите слово: ')
        tmp = transl(word)
        if tmp:
            print('Переводы')
            for i in tmp:
                print(i, end = '; ')
            print()
        else:
            print('Слово не найдено')
        continue

    if cmd == [6]:
        theme = input('Введите название темы: \n')
        if type(create_th(theme)) == int:
            print('Тема уже существует')
        else: print('Тема создана')
        continue

    if cmd == [7]:
        theme = input('Введите название темы для удаления\n')
        # Проверка на существование
        if del_th(theme) == 0:
            print('Темы не существет')
        else:
            print('Удалено!')
        continue

    if cmd == [8]:
        word = input('Введите слово')
        new_word = input('Введите новое слово(пустая строка)')

        changes = input('Введите значения для замены '
                        'между заменяемыми словами "-"'
                        'между парами ";"(пустая строка)').split(';')
        if changes == ['']: changes = []
        else: changes = [pair.split('-') for pair in changes]
        mean = [pair[0] for pair in changes]
        new_mean = [pair[1] for pair in changes]

        theme = input('Введите темы в которых будет произведена замена'
                      '(для разделения ";")пустая строка для все тем').split(';')
        if theme == ['']: theme = scan()

        change(mean,new_mean,word,new_word,*theme)
        print('Завершено')

print('Выполнение программы завершено!\nДо новых встреч!')
