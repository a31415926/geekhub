"""Write a script to concatenate following dictionaries to create a new one."""

dic1={1:10, 2:20}
dic2={3:30, 4:40}
dic3={5:50,6:60}
dic_new={}
dic_new.update(dic1)
dic_new.update(dic2)
dic_new.update(dic3)
print(dic_new)