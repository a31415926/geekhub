"""Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
   Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>)
   і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
   Логіка наступна:
       якщо введено коректну пару ім'я/пароль - вертається <True>;
       якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>, інакше (<silent> == <False>) - породжується виключення LoginException"""
	   
	   
	   
class LoginException(Exception):
	pass
	

def check_user_and_pass(username, password, silent = False):
	data_users = [{'ivan':'pass1', 'petr':'123456', 'oleg':'qwerty', 'nikita':'asdewq', 'igor':'zxcvbn'}]
	
	try:
		if data_users[0][username] == password:
			return True
		else:
			if not silent:
				raise LoginException()
			else:
				return False
	except KeyError:
		if silent:
			return False
		else:
			raise LoginException()
		
		
print(check_user_and_pass('ivasdn','passas1', True))
