"""Написати функцію < fibonacci >, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його."""

def fibonacci(n):
	res = [0, 1, 1]
	if (n>1):
		while True:
			if ((res[-1] + res[-2]) > n):
				break
			else:
				res.append(res[-1]+res[-2])
		return res
	return res


n = int(input())
print(fibonacci(n))		