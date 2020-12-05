import csv
import json
import os
import random


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
per_precent = 10 #вероятность подарка суммой sum_precent при авторизации
sum_precent = 150


def path_file(*args):
	return os.path.join(os.path.dirname(__file__), *args)



def create_structure():
#проверяем путь к файлу с юзерами и создаем структуру, если файла нет.
#в users.csv автоматически добавляем admin и collector

	if not os.path.exists(path_file("users.csv")):
		os.mkdir(path_file("balance"))
		os.mkdir(path_file("transactions"))
		with open(path_file('users.csv'), 'w', newline='') as f:
			fieldnames = ['login', 'password']
			writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
			writer.writeheader()
			writer.writerow({'login':'admin', 'password':'admin'})
			writer.writerow({'login':'collector', 'password':'collector'})
			
			
		default_bills = {}
		default_bills['total'] = 0
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
		
		new_trans = ["id_1",default_balance]
		
		with open(path_file('transactions', 'admin_transactions.csv'), 'w', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=['id', 'transaction'], delimiter='|')
			writer.writeheader()
			writer.writerow({'id':1, 'transaction':default_balance})
			
		with open(path_file('transactions', 'collector_transactions.csv'), 'w', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=['id', 'transaction'], delimiter='|')
			writer.writeheader()
			writer.writerow({'id':1, 'transaction':default_balance})
			

def auth_user():
#авторизация юзера
	users_csv = csv.DictReader(open('users.csv'), delimiter='|')
	dump_users={}
	for row in users_csv:
		dump_users[row['login']] = {'password':row['password']}
		
	count_try = 1 
	print(dump_users)
	while count_try <= count_try_auth:
		login = input('Введи логин: ')
		password = input('Введи пароль: ')
		if login in dump_users:
			if password == dump_users[login]["password"]:
				if per_precent/100 > random.random():
					new_transaction(login, sum_precent)
					print(f"Держи подарок в сумме {sum_precent} на счет.")
				return login
		
		print(f'Логин/пароль не совпадают. У тебя осталось {count_try_auth-count_try} попыток.')
		count_try+=1
	exit()	
	
	
def new_transaction(login, cash = False):
	try: 
		sum_transaction = float(input('Введи сумму: ')) if not cash else cash
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
	with open(path_file('transactions', f'{login}_transactions.csv'), 'r') as f:
		id = int(f.readlines()[-1].split('|')[0])

	logs = sum_transact if sum_transact[0]=='-' else f"+{sum_transact}"
	with open(path_file('transactions', f'{login}_transactions.csv'), 'a', newline='') as f:
		writer = csv.writer(f, delimiter='|')
		writer.writerow([id+1, logs])
		
		
def history_transactions(login):
	with open(path_file('transactions', f'{login}_transactions.csv')) as f:
		file = csv.DictReader(f, delimiter='|')
		for row in file:
			print(row['transaction'])
	


def check_balance(login, ret = False):
	with open(path_file('balance', f'{login}_balance.txt')) as f:
		if ret:
			return f.read()
		print(f.read())
					
				
def exists_user(login):
	with open(path_file('users.csv'), newline='') as f:
		users = csv.DictReader(f, delimiter = '|', fieldnames = ['login', 'password'])
		for i in users:
			if i['login'] == login:
				return True
		
	return False
		

def create_user(login):
	if login == 'admin':
		new_login = input('Логин нового пользователя: ')
		new_pass = input('Пароль нового пользователя: ')
		if not exists_user(new_login):
			with open(path_file('users.csv'), 'a', newline='') as f:
				writer = csv.writer(f, delimiter='|')
				writer.writerow([new_login, new_pass])
			
			with open(path_file('balance', f'{new_login}_balance.txt'), 'w') as f:
				f.write(default_balance)
			with open(path_file('transactions', f'{new_login}_transactions.csv'), 'w', newline = '') as f:
				writer = csv.DictWriter(f, fieldnames=['id', 'transaction'], delimiter='|')
				writer.writeheader()
				writer.writerow({'id':1, 'transaction':default_balance})
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
		
		del(sum_bills['total'])
		for key, old_c in sum_bills.items():
			sum_bills[key] = old_c + count_bill[int(key)]
		
		total_cash = 0
		for key, val in sum_bills.items():
			total_cash+=int(key)*val
		sum_bills['total'] = total_cash
		with open(path_file('bills.json'), 'w') as f:
			json.dump(sum_bills, f)
	
	else:
		print('403')		
		
def check_free_bills():
	with open(path_file('bills.json')) as f:
		check_bills = json.load(f)
	print('Доступно:')
	for key, val in check_bills.items():
		if key == 'total':
			print('Общая сумма: ', val)
		else:
			print(f"{key} грн {val} шт.")
		
def delete_user(login):
	login_for_delete = input('')
	if exists_user(login_for_delete):
		os.remove(path_file('balance', f'{login_for_delete}_balance.txt'))
		os.remove(path_file('transactions', f'{login_for_delete}_transactions.csv'))
		users_csv = csv.DictReader(open('users.csv'), delimiter='|')
		user_db={}
		for row in users_csv:
			user_db[row['login']] = {'password':row['password']}
		del(user_db[login_for_delete])
		with open(path_file('users.csv'), 'w', newline='') as f:
			fieldnames = ['login', 'password']
			writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
			writer.writeheader()
			for key, val in user_db.items():
				writer.writerow({'login': key, 'password':val['password']})
			
		print('User delete')
	else:
		print('403')
		

def change_pass(login):
	new_pass = input('Enter new pass: ')
	users_csv = csv.DictReader(open('users.csv'), delimiter='|')
	user_db={}
	for row in users_csv:
		user_db[row['login']] = {'password':row['password']}
	user_db[login]["password"] = new_pass
	with open(path_file('users.csv'), 'w', newline='') as f:
		fieldnames = ['login', 'password']
		writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
		writer.writeheader()
		for key, val in user_db.items():
			writer.writerow({'login': key, 'password':val['password']})

	print('Пароль изменен')


def change_login(login):
	new_login = input('Enter new login: ')
	if not exists_user(new_login):
		users_csv = csv.DictReader(open('users.csv'), delimiter='|')
		user_db={}
		for row in users_csv:
			user_db[row['login']] = {'password':row['password']}

		password = user_db[login]["password"]
		del(user_db[login])
		user_db[new_login] = {"password":password}
		with open(path_file('users.csv'), 'w', newline='') as f:
			fieldnames = ['login', 'password']
			writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
			writer.writeheader()
			for key, val in user_db.items():
				writer.writerow({'login': key, 'password':val['password']})

			
		os.rename(path_file('balance', f'{login}_balance.txt'), path_file('balance', f'{new_login}_balance.txt'))
		os.rename(path_file('transactions', f'{login}_transactions.csv'), path_file('transactions', f'{new_login}_transactions.csv'))	
		
				
		print('Логин изменен')
		exit()
	else:
		print('Логин занят') 
		


def calculacion_bills(tlst_bills, tsum_cash_out, temp_bills_db):
	rest_sum_cash = tsum_cash_out #остаток, который нужно выдать
	count_min_bills = 0
	temp_lst_user_bills = {}

	for i in tlst_bills:
		for j in sorted(tlst_bills, reverse = True):
			if j%i == 0 and j<=tsum_cash_out:
				#сравнение возможного количества купюр, с доступным
				temp_bill = temp_bills_db[i] if rest_sum_cash//j >= temp_bills_db[i] else rest_sum_cash//j 
				temp_lst_user_bills[j] = temp_bill
				rest_sum_cash -= temp_bill*j
				count_min_bills -= temp_bill*(j/i)
				if rest_sum_cash == 0:
					break
				
					
		if rest_sum_cash == 0:
			break
	return rest_sum_cash, temp_lst_user_bills
		


def cash_out(login):
	sum_cash_out = abs(float(input('Сколько нужно снять: ')))
	if float(check_balance(login, True)) > sum_cash_out:
		
		with open(path_file('bills.json')) as f:
			bills_db = json.load(f)
		
		total_cash_atm = bills_db['total']
		del(bills_db['total'])
		bills_db = dict([int(a), int(b)] for a, b in bills_db.items())
		
		
		if sum_cash_out <= total_cash_atm:
			rest_sum_cash = sum_cash_out #остаток, который нужно выдать
			lst_user_bills = {}
			lst_bills = sorted(list(bills_db.keys()))
			temp_result = {}

			"""
			идем от меньшей купюры к большей. если найдена большая купюра, кратная меньшей - скоращаем.
			например, вместо 5 по 20 берем 1 по 100
			
			"""
			for i in lst_bills:
				temp_bills_db = bills_db.copy()
				if (temp_bills_db[i] >0):
					temp_bills_db[i]-=1
					temp = calculacion_bills(lst_bills, sum_cash_out - i, temp_bills_db)
					if temp[0] == 0:
						lst_user_bills = temp[1]
						lst_user_bills[i] = lst_user_bills.get(i, 0)+1
						#print(lst_user_bills)
						if len(temp_result) ==0:
							temp_result = lst_user_bills
						if sum(list(lst_user_bills.values())) < sum(list(temp_result.values())) or sum(list(temp_result.values())) == 0:
							temp_result = lst_user_bills
						
			
			if len(temp_result) == 0:
				print("Кобминация для снятия не найдено.")
					
			else:
				for key, val in temp_result.items():
					bills_db[key] -= val
				
				total_cash = 0
				for key, val in bills_db.items():
					total_cash+=int(key)*val
				bills_db['total'] = total_cash
				bills_db = dict([f"{a}", b] for a, b in bills_db.items())
				with open(path_file('bills.json'), 'w') as f:
					json.dump(bills_db, f)
				for key, val in lst_user_bills.items():
					print(f'{key} грн {val} шт.') 
					
					
				new_transaction(login, -sum_cash_out)
				
					
		else:
			print('В банкомате нет столько денег :(')
			
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
