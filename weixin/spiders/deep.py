from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from scrapy import Item,Field
from scrapy.selector import Selector

class DeepItem(Item):
    Url = Field()
    Title = Field()


class Deep(CrawlSpider):

    name = 'DeepSpider'

    start_urls = [
        'http://brucedone.com/archives/985'
    ]
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('http://brucedone.com',))),

        # 提取匹配 'ariticle' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('http://brucedone.com/archives/(\d+)',),deny=('http://brucedone.com/archives/(\d+)\?replytocom=(\d+)')),follow=True, callback='parse_item'),

        # Rule(SgmlLinkExtractor(allow=('a/\d+/\d+\.html'), restrict_xpaths=('//div[@class='left']')),
        #      callback='parse_item')
    )

    def parse_item(self,response):
        item = DeepItem()
        item['Url'] = response.url
        selector = Selector(response)
        titles = selector.xpath("body/div[@id='kratos-wrapper']/div[@id='kratos-page']/div[@id='kratos-blog-post']/div[@class='container']/div[@class='row']/section[@id='main']/article/div[1]/header[@class='kratos-entry-header']/h1/text()").extract()
        # titles = box.xpath('./article/div[1]/header[@class='kratos-entry-header']/h1/text()').extract()
        title = ''.join(titles)
        item['Title'] = title
        yield item














