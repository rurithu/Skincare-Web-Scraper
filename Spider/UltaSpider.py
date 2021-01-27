import scrapy
import math
from UltaScrape.items import UltaItem 



class UltaSpider( scrapy.Spider ):
    name = 'ultaSpider'
    allowed_domains = ['ulta.com']

    start_urls = ['https://www.ulta.com/skin-care?N=2707']

    def parse( self, response ):
        # This parse method will get the urls for all categories
        categories = response.xpath('//li[@class="cat-sub-nav"]/ul/li') 

        for category in categories:
            try:
                category_url = response.urljoin(category.xpath('.//a/@href').extract()[0])  
                Product_category = category.xpath('.//a/text()').extract_first().strip()         
            except Exception as e:
                print(e)
                print('category_url, product_category!!!!'*6)
            print(category_url)
            print(Product_category)

            yield scrapy.Request(category_url, callback = self.parse_category, meta={'Product_category':Product_category}) 
        

    def parse_category( self, response ):
        # will get the urls for all pages in each category 
        Product_category = response.meta['Product_category']
        try:
            nproducts=int(response.xpath('//span[@class="search-res-number"]/text()').extract_first())
            npages = math.ceil(nproducts/96)
            next_urls = [response.url+'&No='+str(i*96) +'&Nrpp=96' for i in range(0,npages)]
        except Exception as e:
            print(e)

        for page_url in next_urls:
            yield scrapy.Request(page_url, callback = self.parse_product, meta={'Product_category':Product_category})

    def parse_product( self, response):
        # Want the URL for each product by parsing through the category pages
        Product_category = response.meta['Product_category']
        try:
            product_containers = response.xpath('//div[@class="productQvContainer"]')

        except Exception as e:
            print(e)
        
        for product in product_containers:
            
            try:
                product_url = response.urljoin(product.xpath('.//p[@class="prod-desc"]/a/@href').extract()[0]) ############
            except Exception as e:
                print(e)
            
            try:
                Product_rating = product.xpath('./a//label[@class="sr-only"]/text()').extract_first()
            except:
                Product_rating = None
 
            yield scrapy.Request(product_url, callback = self.parse_info, meta={'Product_category':Product_category, 'Product_rating': Product_rating})


    def parse_info( self, response):
        # This parse method will scrape the information from the product page
        Product_category = response.meta['Product_category']
        Product_rating = response.meta['Product_rating']
        #print('SSSSS'*20)
        try:
            Product_name = response.xpath('//span[@class="Text Text--subtitle-1 Text--left Text--small Text--text-20"]/text()').extract_first()
            Product_price = response.xpath('//div[@class="ProductPricingPanel"]/span/text()').extract_first()
            Product_details = response.xpath('//div[@class="ProductDetail__productContent"]/text()').extract_first()
            Product_ingredients = response.xpath('//*[@id="productDescription"]/div[3]/div[2]/div[2]/div/div/div/text()').extract_first()
        except Exception as e:
            print(e)
        
        item = UltaItem()

        item['Product_category'] = Product_category
        item['Product_name'] = Product_name
        item['Product_price'] = Product_price
        item['Product_rating'] = Product_rating
        item['Product_ingredients'] = Product_ingredients
        item['Product_details'] = Product_details
        
        yield item

