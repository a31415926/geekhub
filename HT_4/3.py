"""На основі попередньої функції створити наступний кусок кода:
   а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)"""
   
   
class UserValidation(Exception):
	pass
   

def check_username_pass(username, password):
	
	if len(username) < 3 or len(username) > 50:
		raise UserValidation('Длина логина должна быть от 3 до 50-ти символов')
	#проверка на наличие цифры
	elif not list(i for i in password if i.isdigit()):
		raise UserValidation('Пароль должен содержать хотя бы одну цифру')
	elif len(password) < 8:
		raise UserValidation('Пароль должен быть не менее 8-ми символов')
	elif username == password:
		raise UserValidation('Логин и пароль не должны совпадать')
	else:
		return True
		
		
data_users = {'qw':'asdasdasd', 'qwertylog1':'qwertylog1', 'qwert':'withoutdig', 'correctu':'correctpass12', 'login':'pass1'}

for key, val in data_users.items():
	print(f'Name: {key}')
	print(f'Password: {val}')
	print('Status: ', end= ' ')
	try:
		if (check_username_pass(key, val)):
			print('OK')
	except UserValidation as err:
		print(err)
		
	print('-------')