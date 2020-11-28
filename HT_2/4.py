"""Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат. 
Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднi, обробляє повернутий ними результат та також повертає результат. 
Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3"""


def c_sum(a, b, c):
	return a+b+c
	
def c_mul(a, b, c):
	return a*b*c
	
def sum_square(a, b, c):
	return a*a + b*b + c*c
	
def finish(a, b, c):
	return c_sum(a, b, c) + c_mul(a, b, c) + sum_square(a, b, c)
	
	
print(finish(1, 3, 5))