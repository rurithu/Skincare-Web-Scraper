# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UltaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Product_category = scrapy.Field()
    Product_name = scrapy.Field()
    Product_price = scrapy.Field()
    Product_rating = scrapy.Field()
    Product_ingredients = scrapy.Field()
    Product_details = scrapy.Field()

