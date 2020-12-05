"""Програма-банкомат.
   Створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) та історію транзакцій (файл <{username}_transactions.data>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено число; знімається не більше, ніж є на рахунку).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - спочатку - логін користувача - програма запитує ім'я/пароль. Якщо вони неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
      - потім - елементарне меню типа:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив :)"""
	  
	  
	  
	  
"""
при первом запуске скрипта, с помощью create_admin() создается юзер admin \ admin и все соотвествующие файлы/директории.
для авторизации есть только три попытки. если неправильно - закрывается программа.
главный юзверь - admin\admin
добавлять новых пользователей можно только с помощью него(вшито в new_user()).
дефолтная сумма со старта задается переменной sum_default

список команд:
check balance - просмотр текущего баланса
transaction - сделать новую транзакцию
check history - просмотр истории
exit - выход
new user - новый юзер (только для админа)
delete user - удаление юзера (полностью вся существующая информация.). только для админа
change password - изменение пароля.
change login - изменение логина. логин admin изменить нельзя!

"""
	  
	  
import json
import os
	  
	  
sum_default = '100'
path = fr'{os.path.dirname(__file__)}'

def input_commands(login):
	command = input('Введи команду: ')
	if command == 'check balance':
		print(check_balance(login))
	elif command == 'transaction':
		transaction(login)
	elif command == 'check history':
		check_history(login)
	elif command == 'new user':
		new_user(login)
	elif command == 'delete user':
		delete_user(login)
	elif command == 'change password':
		change_password(login)
	elif command == 'change login':
		change_login(login)
	elif command == 'exit':
		exit()
		
	else:
		print('я не знаю такой команды')
		

def check_balance(login):
	balance = open(f'{path}\\balance\{login}_balance.txt').read()
	return balance
	
def check_history(login):
	with open(f'{path}\\transactions\{login}_transactions.json') as f:
		history_balance_user = json.load(f)
		
	for id, val in history_balance_user.items():
		print (val)
		
		
def check_exists_user(login):
	with open(fr'{path}\users.json') as f:
		dump_users = json.load(f)
			
	return True if login in dump_users else False


def change_password(login):
	cur_pass = input('Введи текущий пароль')
	with open(fr'{path}\users.json') as f:
		dump_users = json.load(f)
	if cur_pass == dump_users[login]["password"]:
		new_pass = input('Введи новый пароль: ')
		dump_users[login]["password"] = new_pass
		with open(fr'{path}\users.json', 'w') as f:
			json.dump(dump_users, f)
		print('Пароль изменен.')
		
def change_login(login):
	if login != 'admin':
		new_login = input('Введи новый логин:')
		if not check_exists_user(new_login):
			with open(fr'{path}\users.json') as f:
				users = json.load(f)
				
			users[new_login] = users[login]
			del(users[login])
			with open(fr'{path}\users.json', 'w') as f:
				json.dump(users, f)
			os.rename(fr'{path}\balance\{login}_balance.txt', fr'{path}\balance\{new_login}_balance.txt')
			os.rename(fr'{path}\transactions\{login}_transactions.json', fr'{path}\transactions\{new_login}_transactions.json')	
			print('Логин изменен. Тебе нужно заново зайти.')
			exit()
		else:
			print('Такой логин занят.')
	else:
		print('Логин админа изменять нельзя.')


def delete_user(login):
#удалени пользователя.
	if login == 'admin':
		del_login = input('Введите логин пользователя, которого нужно удалить: ')
		if check_exists_user(del_login):
			os.remove(fr'{path}\balance\{del_login}_balance.txt')
			os.remove(fr'{path}\transactions\{del_login}_transactions.json')
			with open(fr'{path}\users.json') as f:
				users = json.load(f)
			del(users[del_login])
			with open(fr'{path}\users.json', 'w') as f:
				json.dump(users, f)
			print('Вся информация о пользователе удалена.')
		else:
			print('Пользвоатель не найден.')
		
	else:
		print('недостаточно прав')
		
def new_user(login):
#создание нового юзверя, только если зашли из-под админа.
	if login == 'admin':
		new_login = input('Введи логин нового юзера: ')
		new_password = input('Введи пароль нового юзера: ')
		with open(fr'{path}\users.json') as f:
			dump_users = json.load(f)
			
		if new_login not in dump_users:
			new_user_info = {"password":new_password}
			dump_users[new_login] = new_user_info
			with open(fr'{path}\users.json', 'w') as f:
				json.dump(dump_users, f)
			bal = open(f'{path}\\balance\{new_login}_balance.txt', 'w')
			bal.write(sum_default)
			bal.close()
			new_trans_db = {"id_1":f"+{sum_default}"}
			with open(f'{path}\\transactions\{new_login}_transactions.json', 'w') as f:
				json.dump(new_trans_db, f)
			print('Юзер создан.')
		else:
			print('Пользователь с таким логином уже существует.')
			
	else: 
		print('недостаточно прав.')




def transaction(login):
	#обрабатывает транзацию.
	try:
		sum_trans = float(input('На сколько изменить баланс: '))
	
		with open(f'{path}\\balance\{login}_balance.txt', 'r+') as f:
			balance = float(f.read())
			if (balance + sum_trans >= 0):
				add_history_transaction(login, str(sum_trans))
				f.seek(0)
				f.write(str(balance + sum_trans))
				f.truncate()
				
			else:
				print('у тебя нет столько денег.')
	except ValueError:
		print('Ты ввел не число')
	
	
def add_history_transaction(login, sum_transaction):
	#добавляем в json новое значение с id транзакции и суммой
	
	with open(f'{path}\\transactions\{login}_transactions.json') as f:
		history_balance = json.load(f)
		
	last_id = len(history_balance)
	#проверяем первый символ, чтобы было более наглядно (явно проставить +)
	sum_transaction = f'+{sum_transaction}' if sum_transaction[0].isdigit() else sum_transaction
	history_balance[f'id_{last_id+1}'] = sum_transaction
	with open(f'{path}\\transactions\{login}_transactions.json', 'w') as f:
		json.dump(history_balance, f)
	

def auth_users(login, password):
	with open(fr'{path}\users.json') as f:
		users = json.load(f)
		
	if login in users:
		return True if users[login]['password'] == password else False
	else:
		return False
			
def input_for_auth():
	count = 0
	while count < 3:
		
		login = input('Введи логин: ')
		password = input('Введи пароль: ')
		if auth_users(login, password):
			break
		print('No!')
		count += 1
	else:
		print('Ты исчерпал свои попытки. Прощай.')
		exit()
	return login
		
def create_admin():
	if not os.path.exists(fr'{path}\users.json'):
		os.mkdir(fr'{path}\balance')
		os.mkdir(fr'{path}\transactions')
		user_admin = {"admin":{"password":"admin"}}
		with open(fr'{path}\users.json', 'w') as f:
			json.dump(user_admin, f)
		bal = open(f'{path}\\balance\\admin_balance.txt', 'w')
		bal.write(sum_default)
		bal.close()
		new_trans_db = {"id_1":f"+{sum_default}"}
		with open(f'{path}\\transactions\\admin_transactions.json', 'w') as f:
			json.dump(new_trans_db, f)

		

def start():
	create_admin()
	login = input_for_auth()
	while True:
		input_commands(login)
	
	
	
	
if __name__ == '__main__':
	start()
