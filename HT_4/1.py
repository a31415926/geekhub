"""Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
   Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>)
   і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
   Логіка наступна:
       якщо введено коректну пару ім'я/пароль - вертається <True>;
       якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>, інакше (<silent> == <False>) - породжується виключення LoginException"""
	   
	   
	   
class LoginException(Exception):
	pass
	

def check_user_and_pass(username, password, silent = False):
	data_users = [{'username':'ivan', 'password':'pass1'}, {'username':'petr',  'password':'123456'}, 
            {'username':'oleg', 'password':'qwerty'}, {'username':'nikita', 'password':'asdewq'}, {'username':'igor', 'password':'zxcvbn'}]
	
	try:
		for i in range(len(data_users)):
			if data_users[i]['username'] == username and data_users[i]['password'] == password:
				return True
				break
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
		
		
assert check_user_and_pass('petr', '123456'), 'petr-123456'
assert check_user_and_pass('oleg','asd', True)==False, 'oleg - asd'
