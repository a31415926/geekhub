import requests
from bs4 import BeautifulSoup
import csv
import os 


"""
скрапер https://quotes.toscrape.com/ с пагинацией (все страницы).
в authors.csv пишется информация про авторов.
в quotes.txt цитата, автор и теги.
"""

url = 'https://quotes.toscrape.com/'
authors_lst = []
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'authors.csv')):
    with open(os.path.join(os.path.dirname(__file__), 'authors.csv'), 'w', newline='',encoding='utf-8') as f:
        authors_csv = csv.DictWriter(f, fieldnames = ['name', 'link', 'born_date', 'born_location'], delimiter='|')
        authors_csv.writeheader()
else:
    with open (os.path.join(os.path.dirname(__file__), 'authors.csv'), 'r',encoding='utf-8') as f:
        authors_csv = csv.DictReader(f, delimiter='|')
        for i in authors_csv:
            if i['name'] not in authors_lst:
                authors_lst.append(i['name'])

with open(os.path.join(os.path.dirname(__file__), 'quotes.txt'), 'w', encoding='utf-8') as f:
    pass




def scrap_info(pager=''):
    toscrape = requests.get(url[:-1]+pager)
    soup_page = BeautifulSoup(toscrape.text, 'lxml')
    quotes = soup_page.select('.quote')
    

    for quote in quotes:
        author = quote.find(class_='author')
        author = author.text
        tags = quote.select_one('.keywords').get('content')
        quote_text = quote.select_one('.text').text
        with open(os.path.join(os.path.dirname(__file__), 'quotes.txt'), 'a', encoding='utf-8') as f:
            f.write(f'author: {author}\ntags: {tags}\n{quote_text}\n\n')

        if author not in authors_lst:
            print(author)
            authors_lst.append(author)
            link = quote.select_one('span a')
            link = url[:-1]+link.get('href')
            author_info = requests.get(link)
            author_info_soup = BeautifulSoup(author_info.text, 'lxml')
            author_info_date = author_info_soup.select_one('.author-born-date')
            author_info_location = author_info_soup.select_one('.author-born-location')
            born_date = author_info_date.text if author_info_date else 'None' 
            born_location = author_info_location.text if author_info_location else 'None'

            
            with open(os.path.join(os.path.dirname(__file__), 'authors.csv'), 'a+', newline='',encoding='utf-8') as f:
                authors_csv = csv.DictWriter(f, fieldnames = ['name', 'link', 'born_date', 'born_location'], delimiter='|')
                authors_csv.writerow({'name': author, 'link': link, 'born_date':born_date, 'born_location': born_location})

    pager_next = soup_page.select_one('.pager .next a')
    if pager_next:
        scrap_info(pager_next.get('href')) 


scrap_info()