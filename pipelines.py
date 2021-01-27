# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from scrapy.exceptions import DropItem

class ProductDataPipeline(object): 
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = sqlite3.connect("ultaProd.db")
        self.curr = self.conn.cursor()

    def create_table(self):
    # Create SQL Table 
        self.curr.execute("""DROP TABLE IF EXISTS Product_Info""")
        self.curr.execute("""CREATE TABLE Product_Info(
            ProductCategory text, 
            ProductDetails text, 
            ProductIngredients text, 
            ProductName text, 
            ProductPrice text, 
            ProductRating text
            )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item): 
    # Store Scraped Values into DB
        myquery ="""INSERT into Product_Info
        (ProductCategory, ProductDetails, ProductIngredients, ProductName, ProductPrice, ProductRating) 
        values (?, ?, ?, ?, ?, ?)
        """
        val = (
            item.get('Product_category'),
            item.get('Product_details'),
            item.get('Product_ingredients'),
            item.get('Product_name'),
            item.get('Product_price'),
            item.get('Product_rating')
        )
        self.curr.execute(myquery, val)
        self.conn.commit()