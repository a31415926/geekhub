"""Написати функцію, яка приймає два параметри: ім'я файлу та кількість символів.
   На екран повинен вивестись список із трьома блоками - символи з початку, із середини та з кінця файлу.
   Кількість символів в блоках - та, яка введена в другому параметрі.
   Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі (наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?)"""
   
   
   
   
"""описание третьего параметра:
для обработки ситуаций, когда четко нельзя выделить середину. 
Если параметр False (по дефолту) - кол-во выводимых символов для середины будет -1.
Если True - кол-во выводимых символов для середины будет +1
"""

import os.path



def func_name(name, length, a=False):
	if not os.path.isfile(name):
		print('File not found')
		return
	f = open(name)
	file_length = len(f.read())
	f.seek(0)
	if length < 0:
		print('длина должна быть не отрицательной')
		return
	if file_length < length:
		print('длина больше допустимой')
		return
	
	print(f'Первые {length} символов:\n{f.read(length)}')
	f.seek(file_length-length)
	print(f'Последние {length} символов:\n{f.read(length)}')
	print(f'Средние {length} символов:')
	if (file_length-length)%2 == 0:
		f.seek((file_length-length)/2)
		print(f.read(length))
		
	else:
		if a:
			f.seek(((file_length-length)/2)-1)
			print(f.read(length+1))
		else:
			f.seek(((file_length-length)/2)+1)
			print(f.read(length-1))
		
		
func_name('for_3.txt', 4, True)