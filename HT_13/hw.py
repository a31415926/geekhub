import os
import sqlite3



"""
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
conn = sqlite3.connect(path_file('atm.db'))
cursor = conn.cursor()
cursor.execute("""CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
													user text, pass text, balance INTEGER DEFAULT 100)""")
cursor.execute("""CREATE TABLE if not exists transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, 
															user_id INTEGER, change INTEGER)""")
cursor.execute("""CREATE TABLE if not exists atm_bill (bill INTEGER PRIMARY KEY, count INTEGER)""")





def create_structure():
#проверяем путь к файлу с юзерами и создаем структуру, если файла нет.

	cursor.execute("SELECT COUNT(id) FROM users;")
	is_exists_admin = cursor.fetchall()
	if is_exists_admin[0][0] == 0:
		cursor.execute("INSERT INTO users (user, pass) VALUES (?, ?)", ('admin', 'admin'))
		cursor.execute("INSERT INTO users (user, pass) VALUES (?, ?)", ('collector', 'collector'))
		conn.commit()
	

def auth_user():
#авторизация юзера

	count_try = 1 
	while count_try <= count_try_auth:
		login = input('Введи логин: ')
		password = input('Введи пароль: ')
		cursor.execute("SELECT id FROM users WHERE user = ? and pass = ?", (login, password))
		user_id = cursor.fetchall()
		if len(user_id):
			return user_id[0][0]
		print(f'Логин/пароль не совпадают. У тебя осталось {count_try_auth-count_try} попыток.')
		count_try+=1
	exit()	
	
	
def new_transaction(user_id, cash = False):
	try: 
		sum_transaction = float(input('Введи сумму: ')) if not cash else cash
		cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id, ))
		balance = cursor.fetchall()
		balance = balance[0][0]
		future_balance = balance + sum_transaction
		if future_balance > 0:
			cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (future_balance, user_id))
			conn.commit()
			add_log_transaction(user_id, sum_transaction)
		else:
			print('Недостаточно средств.')
			
	except ValueError:
		print('Нужно ввести число.')
		


def add_log_transaction(user_id, sum_transact):
	cursor.execute("INSERT INTO transactions (user_id, change) VALUES (?, ?)", (user_id, sum_transact))
	conn.commit()
		
		
def history_transactions(user_id):
	cursor.execute("SELECT change FROM transactions WHERE user_id = ?", (user_id,))
	transactions = cursor.fetchall()
	for transaction in transactions:
		print(transaction[0])
	


def check_balance(user_id, ret = False):
	cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id, ))
	balance = cursor.fetchall()
	balance = balance[0][0]		
	if ret:
		return balance
	print(balance)
				
				
def exists_user(login):
	cursor.execute("SELECT COUNT(id) FROM users WHERE user = ?;", (login,))
	is_user_admin = cursor.fetchall()
	return True if is_user_admin[0][0]else False
		

def create_user(user_id):
	if user_id == 1:
		new_login = input('Логин нового пользователя: ')
		new_pass = input('Пароль нового пользователя: ')
		if not exists_user(new_login):
			cursor.execute("INSERT INTO users (user, pass) VALUES (?, ?)", (new_login, new_pass))
			conn.commit()
			print('Юзер создан')
		else:
			print('Логин занят.')
		
		
	else:
		print('403')	
		
def top_up_atm(user_id):
	if user_id == 2:
		count_bill = {}
		for i in sorted(bills, reverse=True):
			print('Кол-во добавляемых купюр ', i)
			cnt = int(input())
			cursor.execute("INSERT OR REPLACE INTO atm_bill (bill, count) VALUES (?, ?)", (i, cnt))

		conn.commit()
	
	else:
		print('403')		
		
def check_free_bills():
	cursor.execute("SELECT * FROM atm_bill")
	check_bills = cursor.fetchall()
	print('Доступно:')
	for val in check_bills:
		print(f"{val[0]} грн {val[1]} шт.")
		
def delete_user(user_id):
	if user_id == 1:
		login_for_delete = input('')
		if exists_user(login_for_delete):
			cursor.execute("DELETE FROM users WHERE user = ?", (login_for_delete))
			conn.execute()
			print('User delete')
	else:
		print('403')
		

def change_pass(user_id):
	new_pass = input('Enter new pass: ')
	cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_pass, user_id))
	conn.commit()
	print('Пароль изменен')


def change_login(user_id):
	new_login = input('Enter new login: ')
	if not exists_user(new_login):
		cursor.execute("UPDATE users SET user = ? WHERE id = ?", (new_login, user_id))
		conn.commit()
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
		


def cash_out(user_id):
	sum_cash_out = abs(float(input('Сколько нужно снять: ')))
	if float(check_balance(user_id, True)) >= sum_cash_out:
		
		cursor.execute("SELECT * FROM atm_bill")
		bills_db = cursor.fetchall()
		total_cash_atm = 0
		for i in bills_db:
			total_cash_atm+=i[0]*i[1]
		bills_db = dict([i[0], i[1]] for i in bills_db)		

		
		
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
				for key, val in lst_user_bills.items():
					cursor.execute("UPDATE atm_bill SET count = ? WHERE bill = ?", (val, int(key)))
				conn.commit()
				for key, val in lst_user_bills.items():
					print(f'{key} грн {val} шт.') 
					
				new_transaction(user_id, -sum_cash_out)
				
		else:
			print('В банкомате нет столько денег :(')
			
	else:
		print('Средств на вашем счету недостаточно')

	
def list_commands(user_id):
	while True:
		command = input('Введи команду: ')
		if command == 'new transaction':
			new_transaction(user_id)
		elif command == 'top up atm':
			top_up_atm(user_id)
		elif command == 'check balance':
			check_balance(user_id)
		elif command == 'check transactions':
			history_transactions(user_id)	
		elif command == 'new user':
			create_user(user_id)
		elif command == 'delete user':
			delete_user(user_id)
		elif command == 'change password':
			change_pass(user_id)
		elif command == 'change login':
			change_login(user_id)
		elif command == 'cash out':
			cash_out(user_id)		
		elif command == 'check free bills':
			check_free_bills()	
		
		elif command == 'exit':
			exit()
		
		else:
			print('Команда не найдена') 
						

def start():

	create_structure()
	auth_user_id = auth_user()
	list_commands(auth_user_id)
	
	

if __name__ == '__main__':
	start()
