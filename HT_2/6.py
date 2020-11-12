"""Маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" -> просто потицяв по клавi
   Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
-  якщо довжина бульше 50 - > ваша фантазiя """


my_str = 'f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345'

def count_len(text):
	dig_in_str = []
	letter_in_str = []
	for i in text:
		
		if i.isdigit():
			dig_in_str.append(int(i))
		elif i.isalpha():
			letter_in_str.append(i)
			
	if 30 < len(text) < 50:
		print(len(text), len(dig_in_str), len(letter_in_str))
		
	elif len(text) < 30 :
		print(sum(dig_in_str), ''.join(letter_in_str))
	
	else:
		print(f'reverce {my_str[::-1]}')
		
		
count_len(my_str)