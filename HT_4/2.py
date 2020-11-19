"""Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом."""
   
   
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
		
		
print(check_username_pass('wwq', 'qwedsdsd23'))
#print(check_username_pass('loginpass12', 'loginpass12'))
#print(check_username_pass('lo', 'loginpass12'))
#print(check_username_pass('log', 'loginpass'))

