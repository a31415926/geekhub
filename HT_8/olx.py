import requests
from bs4 import BeautifulSoup
import csv
import os 
import time
import re
import random
import urllib3



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



"""
Берутся только обычные объявления, топовые рекламные пропускаем
скрипт парсит все объявления категории (с учетом пагинации)
"""


url = 'https://www.olx.ua'
parse_sitemap = requests.get(url + '/sitemap.xml')
req_soup = BeautifulSoup(parse_sitemap.text, 'lxml')
first_region = req_soup.select_one('loc')
first_region = first_region.text.strip()

#парсим категории с первого региона
lst_cat = requests.get(first_region)
cats_soup = BeautifulSoup(lst_cat.text, 'lxml')
categories = []
for i in cats_soup.select('loc'):
    categories.append(i.text)



if not os.path.exists(os.path.join(os.path.dirname(__file__), 'parse_olx.csv')):
    with open(os.path.join(os.path.dirname(__file__), 'parse_olx.csv'), 'w', newline='',encoding='utf-8') as f:
        authors_csv = csv.DictWriter(f, fieldnames = ['link', 'category', 'price', 'board_title', 'name', 'phone', 'date'], delimiter='|')
        authors_csv.writeheader()


def parse_board(link_cat):
    session = requests.Session()
    req_cat = session.get(link_cat, verify=False)
    entry_soap = BeautifulSoup(req_cat.text, 'lxml')
    all_entries = entry_soap.select('#offers_table.fixed.offers.breakword.redesigned .marginright5.link.linkWithHash.detailsLink')
    for link_entry in all_entries:
        time.sleep(random.uniform(1, 2))
        req_entry = session.get(link_entry.get('href'), verify=False)
        entry_info = BeautifulSoup(req_entry.text, 'lxml')
        entry_category = entry_info.select_one('.inline:last-child .link.nowrap span') #категория материала
        entry_category = entry_category.text if entry_category else ''
        price = entry_info.select_one('.pricelabel .pricelabel__value')
        price = price.text if price else ''
        author_name = entry_info.select_one('.offer-user__actions h4 a')
        author_name = author_name.text.strip() if author_name else 'not found'
        author_phone = ''
        entry_date = entry_info.select_one('.offer-bottombar__item>em>strong')
        entry_date = entry_date.text if entry_date else ''
        entry_title = entry_info.select_one('.offer-titlebox h1')
        entry_title = entry_title.text.strip() if entry_title else 'not found'
        is_phone = entry_info.select_one('.contact-button.link-phone')

        if is_phone:
            token_id_re = re.findall(r"-ID(.*?).html", link_entry.get('href'))
            token_id = token_id_re[0]
            token = entry_info.select_one('.offer-section>script')
            token_res = re.findall(r"var phoneToken = '(.*?)';", str(token))
            headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'referer':link_entry.get('href')}
            req_phone = session.get('https://www.olx.ua/ajax/misc/contact/phone/'+token_id+'/?pt='+token_res[0], headers = headers)
            
            #если попали под 403, ждем немного и идем дальше
            if req_phone.status_code == 403:
                time.sleep(100)
                print(link_entry.get('href'))
                req_phone = session.get('https://www.olx.ua/ajax/misc/contact/phone/'+token_id+'/?pt='+token_res[0], headers = headers)
            
            req_phone_json = req_phone.json()
            author_phone = req_phone_json['value']
            
            #может быть указан не один номер телефона, учитываем это.
            if 'span' in author_phone:
                phone_soup = BeautifulSoup(author_phone, 'lxml')
                temp_phone = phone_soup.select('.block')
                temp_phones = []
                for row in temp_phone:
                    temp_phones.append(row.text)

                author_phone = ', '.join(temp_phones)
        
        with open(os.path.join(os.path.dirname(__file__), 'parse_olx.csv'), 'a+', newline='',encoding='utf-8') as f:
            olx_csv = csv.DictWriter(f, fieldnames = ['link', 'category', 'price', 'board_title', 'name', 'phone', 'date'], delimiter='|')
            olx_csv.writerow({'link': link_entry.get('href'), 'category':entry_category, 'price': price, 'board_title':entry_title, 'name':author_name, 'phone':author_phone, 'date':entry_date})

        
    
    next_page = entry_soap.select_one('.fbold.next.abs.large a.link.pageNextPrev')
    if next_page:
        time.sleep(3)
        parse_board(next_page.get('href'))




for cat_val in categories:
    time.sleep(30)
    parse_board(cat_val)
