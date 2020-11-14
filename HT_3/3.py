"""Написати функцию < is_prime >, яка прийматиме 1 аргумент - число від 0 до 1000, и яка вертатиме True, якщо це число просте, и False - якщо ні."""

def is_prime(n):
	d = 2
	if n == 1:
		return True
	while n%d != 0:
		d+=1
	res = True if (d==n) else False
	return res
	
n = int(input())

print(is_prime(n))