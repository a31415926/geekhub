"""Write a script to generate and print a dictionary that contains a number (between 1 and n) in the form (x, x*x)."""


res = {}
n = 5

for i in range(1, n+1):
	res.setdefault(i, i*i)
	
print(res)