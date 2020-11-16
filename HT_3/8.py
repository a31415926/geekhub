"""Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку. 
Тобто, функція приймає два аргументи: список і величину зсуву 
(якщо ця величина додатня - пересуваємо з кінця на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).
   Наприклад:
       fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
       fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
	   """
	   

def func_name(lst, shift):
	res = []
	for i in range(-shift, len(lst)-shift):
		if i >= len(lst):
			res.append(lst[i-len(lst)])
		else:
			res.append(lst[i])
	return res
		

def func_name1(lst, shift):
	if shift>0:
		for i in range(shift):
			a = lst.pop()
			lst.insert(0, a)
	else:
		for i in range(-shift):
			a = lst.pop(0)
			lst.append(a)		
	return lst
		
fnc = [1, 2, 3, 4, 5, 6, 7]
sh = int(input('На сколько нужно переместить:'))

print(func_name(fnc, sh))
print(func_name1(fnc, sh))
