"""Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку. 
Тобто, функція приймає два аргументи: список і величину зсуву 
(якщо ця величина додатня - пересуваємо з кінця на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).
   Наприклад:
       fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
       fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
	   """
	   

def func_name(lst, shift):
	res = []
	if shift > len(lst):
		shift = shift - len(lst)*(shift//len(lst))
	for i in range(-shift, len(lst)-shift):
		if i >= len(lst):
			res.append(lst[i-len(lst)])
		else:
			res.append(lst[i])
	return res
		

def func_name1(lst, shift):
	""" 
	рабочий однострочный вариант, но менее читабельный
	[lst.insert(0, lst.pop()) for i in range(shift)] if shift>0 else [lst.append(lst.pop(0)) for i in range(-shift)]"""	
	if shift > len(lst):
		shift = shift - len(lst)*(shift//len(lst))
	if shift>0:
		[lst.insert(0, lst.pop()) for i in range(shift)]
	else:
		[lst.append(lst.pop(0)) for i in range(-shift)]	
	
	return lst
		
fnc = [1, 2, 3, 4, 5, 6, 7]
sh = int(input('На сколько нужно переместить:'))

print(func_name(fnc, sh))
print(func_name1(fnc, sh))
