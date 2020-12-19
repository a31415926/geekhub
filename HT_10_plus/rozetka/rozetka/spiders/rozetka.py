import scrapy
from rozetka.items import RozetkaItem


class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    headers = {'user-agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    allowed_domains = ['https://rozetka.com.ua']
    start_urls = [
        'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id=4627129']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.pages_category,
                dont_filter=True,
                headers=self.headers
            )

    def pages_category(self, response):
        req_json = response.json()
        total_pages = req_json['data']['total_pages']
        ids = req_json['data']['ids']

        for id_page in range(1, total_pages+1):
            url = f'{self.start_urls[0]}&page={id_page}'
            yield scrapy.Request(
                url=url,
                callback=self.ids_goods_pages,
                dont_filter=True,
                headers=self.headers
            )

    def ids_goods_pages(self, response):
        req_json = response.json()
        ids = req_json["data"]["ids"]
        ids = ','.join((str(i) for i in ids))
        url = f'https://xl-catalog-api.rozetka.com.ua/v3/goods/getDetails?front-type=xl&product_ids={ids}'

        yield scrapy.Request(
            url=url,
            callback=self.goods_info,
            dont_filter=True,
            headers=self.headers
        )

    def goods_info(self, response):
        resp = response.json()
        for good in resp['data']:
            item = RozetkaItem()
            item['id'] = good['id']
            item['category_id'] = good['category_id']
            item['link'] = good['href']
            item['title'] = good['title']
            item['brand'] = good['brand']
            item['images'] = ','.join(good['images']['all_images'])
            item['price'] = good['price']
            item['old_price'] = good['old_price']
            yield item