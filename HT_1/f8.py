"""Write a script to replace last value of tuples in a list."""

simple = [(10, 20, 40), (40, 50, 60), (70, 80, 90)]
val_replace = 100
repl = []
for i in simple:
	repl.append(i[:-1] + (val_replace,))
	
print(repl)