"""Ну і традиційно -> калькулятор :) 
повинна бути 1 ф-цiя яка б приймала 3 аргументи - один з яких операцiя, яку зробити!"""

def calc(a, b, operation):
	if operation == '+':
		return a+b
	elif operation == '-':
		return a-b
	elif operation == '*':
		return a*b
	elif operation == '/':
		if b == 0:
			return 'ишь какой хитрый'
		else: 
			return a/b
	
	

a = int(input('enter first digital:'))
operation = input('enter operation with digitals:')
b = int(input('enter second digita:'))

print(calc(a, b, operation))