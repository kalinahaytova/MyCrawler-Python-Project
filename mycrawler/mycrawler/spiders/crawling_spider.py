import scrapy
from mycrawler.items import CategoryItem
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider


class CrawlingSpider(CrawlSpider):
   
    name = "mycrawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    #Crawler starter
    def parse_start(self, response):

        #Gets all the cateogories in the main url
        for cat in response.xpath('//ul//li//ul//a'):  
            loader = ItemLoader(CategoryItem(), selector=cat) 
            loader.add_xpath('category_name',
                             './text()')  
            url = cat.xpath('.//@href').get()  
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_category,  
                cb_kwargs={'loader': loader}
            )

    #Parses a category page response
    def parse_category(self, response, loader):

        #Gets total count in a category
        total_count = response.xpath('//strong/text()')[1].get()  
        loader.add_value('total_count', total_count)
        
        #The following variables are being initiated to evaluate the relevant values
        price = -1
        book_name = ''
        human_count = 0
        idea_count = 0
        dark_count = 0
        school_count = 0
       
       #Loop goes through each book on the category page, to get the highest price, and other words counts
        for book in response.xpath('//article'):
            price_cur = float(book.xpath('.//div[2]/p/text()').get().strip('£'))  
            if price_cur > price:  
                price = price_cur
                book_name = book.xpath('.//a/text()').get() 
            title = book.xpath('.//a/text()').get()  
            if 'human' in title.lower():
                human_count += 1
            if 'idea' in title.lower():
                idea_count += 1
            if 'dark' in title.lower():
                dark_count += 1
            if 'school' in title.lower():
                school_count += 1

        next_page = response.css('.next a').get()  
        if next_page is not None:
            next_page = response.css('.next a').attrib['href']  
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_details, 

                cb_kwargs={'loader': loader, 'price': price, 'book_name': book_name, 'human_count': human_count,
                           'idea_count': idea_count, 'dark_count': dark_count, 'school_count': school_count}
            )
        else:
            loader.add_value('most_expensive_book', book_name)
            loader.add_value('human_count', human_count)
            loader.add_value('idea_count', idea_count)
            loader.add_value('dark_count', dark_count)
            loader.add_value('school_count', school_count)
            yield loader.load_item()

    def parse_details(self, response, loader, price, book_name, human_count, idea_count, dark_count, school_count):
        for book in response.xpath('//article'):
            price_cur = float(book.xpath('.//div[2]/p/text()').get().strip('£'))
            if price_cur > price:
                price = price_cur
                book_name = book.xpath('.//a/text()').get()
            title = book.xpath('.//a/text()').get()
            if 'human' in title.lower():
                human_count += 1
            if 'idea' in title.lower():
                idea_count += 1
            if 'dark' in title.lower():
                dark_count += 1
            if 'school' in title.lower():
                school_count += 1

        next_page = response.css('.next a').get()
        if next_page is not None:
            next_page = response.css('.next a').attrib['href']
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_details,
                cb_kwargs={'loader': loader, 'price': price, 'book_name': book_name, 'human_count': human_count,
                           'idea_count': idea_count, 'dark_count': dark_count, 'school_count': school_count}
            )
        else:
            loader.add_value('most_expensive_book', book_name)
            loader.add_value('human_count', human_count)
            loader.add_value('idea_count', idea_count)
            loader.add_value('dark_count', dark_count)
            loader.add_value('school_count', school_count)
            yield loader.load_item()

    parse_start_url = parse_start
