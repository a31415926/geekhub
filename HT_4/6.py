"""Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: https://docs.python.org/3/library/stdtypes.html#range"""
   


"""это ужасная реализация, но пока лучше не придумал. но оно работает вроде бы"""
def custom_range(stop, start = 0, step = 1):
	lst = []
	if step == 0:
		return
	if start == 0:
		while True:
			lst.append(start)
			if lst[-1] + step >= stop:
				break
			start += step
	else:
		while True:
			if stop>start and step>0:
				break
			else: 
				lst.append(stop)
				if step>0:
					if lst[-1] + step >= start:
						break
					stop += step
				else: 
					if lst[-1] + step <= start:
						break
					stop += step
	for i in lst:
		yield i
		
for i in custom_range(40, 1, -3):
	print(i)