class Person():

    def __init__(self, age, name):
        self.age = age
        self.name = name

    def show_age(self):
        return self.age

    def print_name(self):
        return self.name

    @property
    def show_all_information(self):
        return self.__dict__


    
a = Person(10, 'Dima')
b = Person(20, 'NeDima')
a.profession = 'Lorem'
b.profession = 'Ispam'


print('exc a:\n', a.show_all_information)
print(a.show_age())

print('exc b\n', b.print_name())
print(b.show_all_information)