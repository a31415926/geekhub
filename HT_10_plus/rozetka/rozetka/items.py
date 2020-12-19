import scrapy


class RozetkaItem(scrapy.Item):
    id = scrapy.Field()
    category_id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
