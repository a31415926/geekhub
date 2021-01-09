class Paper:

    all_paper = {'book':[], 'newspaper':[], 'directory':[] }
    

    def del_paper(self, types, id):
        for n in range(0, len(self.all_paper[types])):
            if self.all_paper[types][n]['id'] == id:
                del(self.all_paper[types][n])
                return True
        return False

    def take_paper(self, types, id):
        for n in range(0, len(self.all_paper[types])):
            if self.all_paper[types][n]['id'] == id:
                self.all_paper[types][n]['stock']-=1
                return True
        return False



class Book(Paper):
    
    def __init__(self):
        pass

    def add(self, genre, author, title):
        book_info = {}
        book_info['id'] = self.all_paper['book'][-1]['id'] + 1 if self.all_paper['book'] else 1
        book_info['title'] = title
        book_info['author'] = author
        book_info['genre'] = genre
        book_info['stock'] = 1
        self.all_paper['book'].append(book_info)

    def del_book(self, id):
        self.del_paper('book', id)

    def take_book(self, id):
        self.take_paper('book', id)


    @property
    def check_all_books(self):
        return self.all_paper['book']

class Newspaper(Paper):
    
    def __init__(self):
        pass

    def add(self, title):
        newspaper_info = {}
        newspaper_info['id'] = self.all_paper['newspaper'][-1]['id'] + 1 if self.all_paper['newspaper'] else 1
        newspaper_info['title'] = title
        newspaper_info['stock'] = 1
        self.all_paper['newspaper'].append(newspaper_info)

    def del_newspaper(self, id):
        self.del_paper('newspaper', id)

    def take_newspaper(self, id):
        self.take_paper('newspaper', id)

    @property
    def check_all_newspaper(self):
        return self.all_paper['newspaper']


class Directory(Paper):
    
    def __init__(self):
        pass

    def add(self, title, subj):
        directory_info = {}
        directory_info['id'] = self.all_paper['directory'][-1]['id'] + 1 if self.all_paper['directory'] else 1
        directory_info['title'] = title
        directory_info['subj'] = subj
        directory_info['stock'] = 1
        self.all_paper['directory'].append(directory_info)

    def del_directory(self, id):
        self.del_paper('directory', id)

    def take_directory(self, id):
        self.take_paper('directory', id)

    @property
    def check_all_directory(self):
        return self.all_paper['directory']


books = Book()
books.add('Фантастика', 'Иван Петров', 'Лучшая фантастика')
book_two = Book().add('Комедия', 'Сидоров', 'А тут комедия')
Book().add('СуперЖанр', 'Жуков', 'Лучшая книга')
print(*Book().check_all_books)
Book().del_book(2)
Book().take_book(3)
print(*Book().check_all_books)
Newspaper().add('NewsPaper Title')
Directory().add('Directory Title', 'test')

for key, val in Directory().all_paper.items():
    print('\n'+key)
    for temp_val in val:
        print('\n')
        for i, j in temp_val.items():
            print(i, j, sep=': ')
            