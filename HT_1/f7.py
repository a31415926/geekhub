"""Write a script to concatenate all elements in a list into a string and print it."""

elements = ['test_a', 'Hello', 'people', 5, 'wow']

#переводим все в строку, что бы не было TypeError при использовании числа
elements = list(map(str, elements))
print(' '.join(elements))