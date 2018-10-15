# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from scrapy import Item, Field


def remove_whitespace(value):
    return value.strip()


class DekaSupremecourtItem(Item):
    # define the fields for your item here like:
    title = Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst()
    )
    content = Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst()
    )
