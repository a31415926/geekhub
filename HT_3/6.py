"""Вводиться число. Якщо це число додатне, знайти його квадрат, якщо від'ємне, збільшити його на 100, якщо дорівнює 0, не змінювати."""

def func_name(n):
	res = n
	if n > 0:
		res = n*n
	elif n < 0:
		res = n+100
	else:
		res = n
		
	return res
	
n = float(input())
print(func_name(n))