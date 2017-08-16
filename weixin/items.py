# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field

class HotWordItem(Item):
    HotWord = Field()
    HotWordType = Field()  # 词源---热词类型            例如：汽车，美食
    BDHotWordLink = Field()
    WXHotWordLink = Field()
    WBHotWordLink = Field()

class NewsItem(Item):
    FromWord = Field()          # 来自哪个热词        例如：乐天，特斯拉
    Title = Field()
    TitleLink = Field()
    Summary = Field()


class TigerItem(Item):
    Url = Field()
    Title = Field()
    Author = Field()
    Date = Field()
    Source = Field()
    Audio = Field()
    Voice = Field()
    Img = Field()
    Content = Field()

