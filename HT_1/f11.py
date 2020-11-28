"""Write a script to remove duplicates from Dictionary."""


dic = {'one': 'qwerty', 'name':'Dmitry', 'f_name':'Dmitry', 'two':'z'}

res = {}
for i, k in dic.items():
	if k not in res.values():
		res[i] = k

print(res)