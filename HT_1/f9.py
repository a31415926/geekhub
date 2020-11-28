"""Write a script to remove an empty tuple(s) from a list of tuples."""

sample_data = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
expected_data = []
for i in sample_data:
	if len(i)>0:
		expected_data.append(i)
		
print(expected_data)