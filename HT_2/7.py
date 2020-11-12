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
	
	
print('enter first digital:')
a = int(input())
print('enter operation with digitals:')
operation = input()
print('enter second digita:')
b = int(input())

print(calc(a, b, operation))