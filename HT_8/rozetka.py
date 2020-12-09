import csv
import requests
import json
import os 
from time import sleep




def get_all_ids_goods(id_cat):
    
    req = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id={id_cat}')
    if req.status_code == 200:
        all_request = req.json()
        ids_goods = all_request['data']['ids']
        get_goods_info(ids_goods, id_cat)
        total_pages_category = all_request['data']['total_pages']
        for id_page in range(2, total_pages_category+1):
            sleep(1)
            req_for_get_id_goods = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id={id_cat}&page={id_page}')
            if req_for_get_id_goods.status_code == 200:
                temp_ids_goods = req_for_get_id_goods.json()
                get_goods_info(temp_ids_goods, id_cat)
                ids_goods += temp_ids_goods['data']['ids']

    else:
        print('Категория не найдена. Попробуй ввести другой ID', req.url)
            

        
def get_goods_info(lst_ids, id_category):
    req_goods = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/getDetails?product_ids={lst_ids}')
    if req_goods.status_code == 200:
        all_goods = req_goods.json()
        all_goods = all_goods['data']
        good_info = {}
        for good in all_goods:
            #собираем нужную инфу про товар
            good_info['id'] = good.get('id')
            good_info['title'] = good.get('title')
            good_info['cat_id'] = good.get('category_id')
            good_info['brand'] = good.get('brand')
            good_info['desc'] = good.get('docket').replace('\n', '').replace('\r', '')
            good_info['href'] = good.get('href')
            good_info['images'] = ','.join(good['images']['all_images']) if good.get('images') else ''
            good_info['price'] = good.get('price')
            good_info['old_price'] = good.get('old_price')
            good_info['status'] = good.get('status')

            write_goods_in_file(id_category, good_info)



def create_file_with_goods(id_cat_with_file):
    #создаем csv файл с айдишкой категории
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f'{id_cat_with_file}_products.csv')):
        with open(os.path.join(os.path.dirname(__file__), f'{id_cat_with_file}_products.csv'), 'w', newline='',encoding='utf-8') as f:
            fields = ['id', 'title', 'cat_id', 'brand', 'desc', 'href', 'images', 'price', 'old_price', 'status']
            products_csv = csv.DictWriter(f, fieldnames = fields, delimiter='\\')
            products_csv.writeheader()


def write_goods_in_file(id_category, good_all_info):
    with open(os.path.join(os.path.dirname(__file__), f'{id_category}_products.csv'), 'a+', newline = '', encoding='utf-8') as f:
        fields = ['id', 'title', 'cat_id', 'brand', 'desc', 'href', 'images', 'price', 'old_price', 'status']
        products_csv = csv.DictWriter(f, fieldnames = fields, delimiter='\\')
        products_csv.writerow({'id':good_all_info['id'], 'title':good_all_info['title'], 
                                'cat_id':good_all_info['cat_id'], 'brand':good_all_info['brand'], 
                                'desc':good_all_info['desc'], 'href':good_all_info['href'],
                                'images':good_all_info['images'], 'price':good_all_info['price'], 
                                'old_price':good_all_info['old_price'], 'status':good_all_info['status']})


def main():
    id_category = input('Введи ID категории: ')
    create_file_with_goods(id_category)
    get_all_ids_goods(id_category)




if __name__ == "__main__":
    main()

