# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field


# used for striping the value category name
def strip_value(value):
    return value.strip()

class CategoryItem(scrapy.Item):
    category_name = Field(input_processor=MapCompose(strip_value), output_processor=TakeFirst())
    total_count = Field(output_processor=TakeFirst())
    most_expensive_book = Field(output_processor=TakeFirst())
    human_count = Field(output_processor=TakeFirst())
    idea_count = Field(output_processor=TakeFirst())
    dark_count = Field(output_processor=TakeFirst())
    school_count = Field(output_processor=TakeFirst())
