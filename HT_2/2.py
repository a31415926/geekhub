"""Користувачем вводиться початковий і кінцевий рік. Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно)."""

start = int(input())
finish = int(input())

for i in range(start, finish+1):
	if i%400 == 0:
		print(i)
		
	elif i%4 == 0 and i%100 != 0:
		print(i)