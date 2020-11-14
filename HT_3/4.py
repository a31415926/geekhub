"""Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих чисел всередині цього діапазона."""

def prime_list(start, finish):
	res = []
	for i in range(start, finish+1):
		d = 2
		#чтобы не было бесконечного цикла
		if i == 1:
			res.append(1)
		else:
			while i%d!=0:
				d+=1
			if d==i:
				res.append(i)
	return res
	

start = int(input('start:'))
finish = int(input('finish:'))

print(prime_list(start, finish))
