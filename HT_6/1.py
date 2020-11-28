import json
import os




"""
обновленная версия (с поддержкой убунты, проверено :) )
при первом запуске программы создается вся структура и первых два юзера: админ и инкасатор.

инкасатор - имеет права обычного пользователя, но с возможностью добавления денег в банкомат. добавляется автоматически
файл баланса - сумма на карте. пополнить можно на любую сумму, это никак не связано с банкоматом.
в банкомат может добавить деньги только инкасатор.

список функций в list_command

cash_out - снять с банкомата

"""


default_balance = '1000'
bills = [20, 50, 100, 200, 500, 1000] #cписок купюр
count_try_auth = 3


def path_file(*args):
	return os.path.join(os.path.dirname(__file__), *args)



def create_structure():
#проверяем путь к файлу с юзерами и создаем структуру, если файла нет.
#в users.json автоматически добавляем admin и collector

	if not os.path.exists(path_file("users.json")):
		os.mkdir(path_file("balance"))
		os.mkdir(path_file("transactions"))
		default_users = {"admin":{"password":"admin"}, "collector":{"password":"collector"}}
		with open(path_file('users.json'), 'w') as f:
			json.dump(default_users, f)
			
		default_bills = {}
		for i in sorted(bills, reverse=True):
			default_bills[i] = 0
		with open(path_file('bills.json'), 'w') as f:
			json.dump(default_bills, f)
			
		admin_balance = open(path_file('balance', 'admin_balance.txt'), 'w')
		admin_balance.write(default_balance)
		admin_balance.close()
		
		collector_balance = open(path_file('balance', 'collector_balance.txt'), 'w')
		collector_balance.write(default_balance)
		collector_balance.close()		
		
		new_trans = {"id_1":f"+{default_balance}"}
		
		with open(path_file('transactions', 'admin_transaction.json'), 'w') as f:
			json.dump(new_trans, f)
		with open(path_file('transactions', 'collector_transaction.json'), 'w') as f:
			json.dump(new_trans, f)
			

def auth_user():
#авторизация юзера
	with open(path_file('users.json')) as f:
		dump_users = json.load(f)
		
	count_try = 1 
	while count_try <= count_try_auth:
		login = input('Введи логин: ')
		password = input('Введи пароль: ')
		if login in dump_users:
			if password == dump_users[login]["password"]:
				return login
		
		print(f'Логин/пароль не совпадают. У тебя осталось {count_try_auth-count_try} попыток.')
		count_try+=1
	exit()	
	
	
def new_transaction(login, cash = False):
	try: 
		sum_transaction = float(input('Введи сумму: ')) if not cash else -cash
		with open(path_file('balance', f'{login}_balance.txt'), 'r+') as f:
			balance = float(f.read())
			if balance + sum_transaction > 0:
				f.seek(0)
				f.write(str(balance+sum_transaction))
				f.truncate()
				add_log_transaction(login, str(sum_transaction))
			else:
				print('Недостаточно средств.')
			
	except ValueError:
		print('Нужно ввести число.')
		


def add_log_transaction(login, sum_transact):
	with open(path_file('transactions', f'{login}_transaction.json')) as f:
		logs = json.load(f)
	
	logs[f"id_{len(logs)+1}"] = sum_transact if sum_transact[0]=='-' else f"+{sum_transact}"
	with open(path_file('transactions', f'{login}_transaction.json'), 'w') as f:
		json.dump(logs, f)
		
		
def history_transactions(login):
	with open(path_file('transactions', f'{login}_transaction.json')) as f:
		transactions = json.load(f)
	print(list(transactions.values()), sep='\n')
	


def check_balance(login, ret = False):
	with open(path_file('balance', f'{login}_balance.txt')) as f:
		if ret:
			return f.read()
		print(f.read())
					
				
def exists_user(login):
	with open(path_file('users.json')) as f:
		users = json.load(f)
	return True if login in users else False
		

def create_user(login):
	if login == 'admin':
		new_login = input('Логин нового пользователя: ')
		new_pass = input('Пароль нового пользователя: ')
		if not exists_user(new_login):
			with open(path_file('users.json')) as f:
				users=json.load(f)
			users[new_login] = {"password":new_pass}
			with open(path_file('users.json'), 'w') as f:
				json.dump(users, f)
			
			with open(path_file('balance', f'{new_login}_balance.txt'), 'w') as f:
				f.write(default_balance)
			with open(path_file('transactions', f'{new_login}_transactions.json'), 'w') as f:
				json.dump({"id_1":f"+{default_balance}"}, f)
			print('Юзер создан')
		else:
			print('Логин занят.')
		
		
	else:
		print('403')	
		
def top_up_atm(login):
	if login == 'collector':
		count_bill = {}
		for i in sorted(bills, reverse=True):
			print('Кол-во добавляемых купюр ', i)
			count_bill[i] = int(input())
		with open(path_file('bills.json')) as f:
			sum_bills = json.load(f)
		
		
		for key, old_c in sum_bills.items():
			sum_bills[key] = old_c + count_bill[int(key)]
		
		with open(path_file('bills.json'), 'w') as f:
			json.dump(sum_bills, f)
	
	else:
		print('403')		
		
def check_free_bills():
	with open(path_file('bills.json')) as f:
		check_bills = json.load(f)
	print('Доступно:')
	for key, val in check_bills.items():
		print(f"{key} грн {val} шт.")
		
def delete_user(login):
	login_for_delete = input('')
	if exists_user(login_for_delete):
		os.remove(path_file('balance', f'{login_for_delete}_balance.txt'))
		os.remove(path_file('transactions', f'{login_for_delete}_transaction.json'))
		with open(path_file('users.json')) as f:
			user_db = json.load(f)
		del(user_db[login_for_delete])
		with open(path_file('users.json'), 'w') as f:
			json.dump(user_db, f)
		print('User delete')
	else:
		print('403')
		

def change_pass(login):
	new_pass = input('Enter new pass: ')
	with open(path_file('users.json')) as f:
		user_db = json.load(f)
	
	user_db[login]["password"] = new_pass
	with open(path_file('users.json'), 'w') as f:
		json.dump(user_db, f)
	print('Пароль изменен')


def change_login(login):
	new_login = input('Enter new login: ')
	if not exists_user(new_login):
		with open(path_file('users.json')) as f:
			user_db = json.load(f)
		
		password = user_db[login]["password"]
		del(user_db[login])
		user_db[new_login] = {"password":password}
		
		with open(path_file('users.json'), 'w') as f:
			json.dump(user_db, f)
		
		os.rename(path_file('balance', f'{login}_balance.txt'), path_file('balance', f'{new_login}_balance.txt'))
		os.rename(path_file('transactions', f'{login}_transactions.json'), path_file('transactions', f'{new_login}_transactions.json'))	
		
				
		print('Логин изменен')
		exit()
	else:
		print('Логин занят') 
		
def cash_out(login):
	sum_cash_out = abs(float(input('Сколько нужно снять: ')))
	if float(check_balance(login, True)) > sum_cash_out:
		
		with open(path_file('bills.json')) as f:
			bills_db = json.load(f)
		
		
		bills_db = dict([int(a), int(b)] for a, b in bills_db.items())
		rest_mon = 0
		for key, val in bills_db.items():
			rest_mon+=key*val
		
		if sum_cash_out <= rest_mon:
			rest_sum_cash = sum_cash_out #остаток, который нужно выдать
			lst_user_bills = {}
			lst_bills = sorted(list(bills_db.keys()))
			count_min_bills = 0
		
			"""
			идем от меньшей купюры к большей. если найдена большая купюра, кратная меньшей - скоращаем.
			например, вместо 5 по 20 берем 1 по 100
			
			"""
			for i in lst_bills:
				for j in sorted(lst_bills, reverse = True):
					if j%i == 0 and j<=sum_cash_out:
						#сравнение возможного количества купюр, с доступным
						temp_bill = bills_db[i] if rest_sum_cash//j >= bills_db[i] else rest_sum_cash//j 
						lst_user_bills[j] = temp_bill
						rest_sum_cash -= temp_bill*j
						count_min_bills -= temp_bill*(j/i)
						if rest_sum_cash == 0:
							break
				if rest_sum_cash == 0:
					break
			
			
			if rest_sum_cash != 0:
				#если не сработало, идем по жадному способу
				rest_sum_cash = sum_cash_out
				lst_user_bills = {}
				for key, val in bills_db.items():
					if rest_sum_cash//key > 0:
						lst_user_bills[key] = val if rest_sum_cash//key > val else rest_sum_cash//key
						rest_sum_cash -= lst_user_bills[key]*key
					
					if rest_sum_cash == 0:
						break
				
				if rest_sum_cash != 0:
					print("Кобминация для снятия не найдено.")
					
				else:
					for key, val in lst_user_bills.items():
						bills_db[key] -= val
					bills_db = dict([f"{a}", b] for a, b in bills_db.items())
					with open(path_file('bills.json'), 'w') as f:
						json.dump(bills_db, f)
						
					new_transaction(login, sum_cash_out)
					
					for key, val in lst_user_bills.items():
						print(f'{key} грн {val} шт.') 
					
			else:
				for key, val in lst_user_bills.items():
					bills_db[key] -= val
				bills_db = dict([f"{a}", b] for a, b in bills_db.items())
				with open(path_file('bills.json'), 'w') as f:
					json.dump(bills_db, f)
				for key, val in lst_user_bills.items():
						print(f'{key} грн {val} шт.') 
					
					
				new_transaction(login, sum_cash_out)
				
					
						
			
	else:
		print('Средств на вашем счету недостаточно')

	
def list_commands(login):
	while True:
		command = input('Введи команду: ')
		if command == 'new transaction':
			new_transaction(login)
		elif command == 'top up atm':
			top_up_atm(login)
		elif command == 'check balance':
			check_balance(login)
		elif command == 'check transactions':
			history_transactions(login)	
		elif command == 'new user':
			create_user(login)
		elif command == 'delete user':
			delete_user(login)
		elif command == 'change password':
			change_pass(login)
		elif command == 'change login':
			change_login(login)
		elif command == 'cash out':
			cash_out(login)		
		elif command == 'check free bills':
			check_free_bills()	
		
		elif command == 'exit':
			exit()
		
		else:
			print('Команда не найдена') 
						

def start():

	create_structure()
	auth_login = auth_user()
	list_commands(auth_login)
	
	

if __name__ == '__main__':
	start()
