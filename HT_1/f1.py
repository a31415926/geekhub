"""Write a script which accepts a sequence of comma-separated numbers 
from user and generate a list and a tuple with those numbers."""

numbers = input()
num_list = list(map(str, numbers.split(', ')))
num_tuple = tuple(map(str, numbers.split(', ')))

print(num_set)
print(num_tuple)