"""Написати функцiю season, яка приймає один аргумент — номер мiсяця (вiд 1 до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)"""

def season(mounth):
	if 1 <= mounth <= 2 or mounth == 12:
		return 'зима'
	elif 3<=mounth<=5:
		return 'весна'
	elif 6<=mounth<=8:
		return 'лето'
	elif 9<=mounth<=11:
		return 'осень'
	else:
		return 'месяц введен неправильно'
		
		
n_mounth = int(input())
print (season(n_mounth))