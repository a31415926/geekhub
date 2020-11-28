"""Написати функцію, яка приймає на вхід список і підраховує кількість однакових елементів у ньому."""

def func_name(lst):
	res = {}
	for i in lst:
		if i not in res:
			res[i] = lst.count(i)
				
	return res
	
lst = [1, 3, 5, 6, 2, 1, 100, 1, 30, 3, 5, 100]

print(func_name(lst))