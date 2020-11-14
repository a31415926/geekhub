"""Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ."""

def square(side_len):
	p_square = side_len*4
	s_square = side_len**2
	d_square = side_len*2**0.5
	res_square = (p_square, s_square, d_square)
	return res_square
	
	
squ = float(input())
print(square(squ))