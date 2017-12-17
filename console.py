# Вывод меню на экран
def print_menu():
	print('='*30,'МЕНЮ','='*30)
	print('1. Список слов')
	print('2. Тестирование')
	print('3. Добавление слова')
	print('4. Удаление слова')
	print('5. Перевод слова')
	print('6. Cоздание темы')
	print('7. Удаление темы')
	print('8. Изменение слова')
	print('0. Завершение программы')
	print('\n')

# Чтение команды
def read_cmd(s = 'Введите номер режима\n',err = 'Введен неверный режим!'):
	res = input(s).split()
	if res == ['']: return res
	for i in range(len(res)):
		if res[i].isdigit():
			res[i] = int(res[i])
		else:
			print(err)
			res = -1
			break
	return res