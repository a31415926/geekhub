"""Write a script to convert decimal to hexadecimal"""


numbers = list(map(lambda x:hex(int(x))[2:], input().split(', ')))
numbers_hex = ', '.join(numbers)
print (numbers_hex)