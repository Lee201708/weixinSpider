'''
创建日期：2017.4.17
创建人：Lee
功能：从新闻详情页中获取数据。标题-作者-正文-图片链接-视频链接

'''

from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
from weixin.items import TigerItem
import logging

class wxNews(RedisSpider):
    name = 'wxMediaSpider'
    # logging.basicConfig(filename='logs/WXMediaSpiderInfologger.log', level=logging.INFO)
    custom_settings = {
        'ITEM_PIPELINES':{
            'weixin.pipelines.JsonWritePipeline':200,
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Cache-Control':'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'mp.weixin.qq.com',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': 'http://weixin.sogou.com/'
        }
    }

    # rules = (
    #     # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
    #     Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),
    #
    #     # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
    #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    # )

    redis_key = 'WXMedia:urls'
    # start_urls = [
    #    'http://mp.weixin.qq.com/s?src=3&timestamp=1491815197&ver=1&signature=uCGvM5PVD3HQtvGPxFuwl3nghVZnW9ZUQgTr8dHihIjj-5xHiCU7uJvS4nyJO5jAf-AmOH54s3XckHHBArkGGc2J0v1De2o*hM6VpvSmKdPUtfkM-Oy0a5Ff2ibSDzf1*nnmtUXh7xPEBP9OJRNDVZO5YENwcA1lF*0ITJ24De4='
    # ]
    '''
    response.url获取的都是临时地址，会过期。
    加&devicetype=Windows-QQBrowser&version=61030004&pass_ticket=qMx7ntinAtmqhVn+C23mCuwc9ZRyUp20kIusGgbFLi0=&uin=MTc1MDA1NjU1&ascene=1
    重定向到永久地址
    '''
    def parse(self, response):
        if not response.body:
            print('there is no response.body,please go and check it ')
            return
        else:
            selector = Selector(response)
            rich_media = selector.xpath('.//div[@class="rich_media"]')
            if rich_media ==[]:
                print('%s 内容为空,已过期或被举报' %response.url)
                return
            else:
                title = ''.join(selector.xpath('.//h2[@class="rich_media_title"]/text()').extract()).strip()
                meta_list = selector.xpath('.//div[@class="rich_media_meta_list"]')
                date = ''.join(meta_list.xpath('.//em[@class="rich_media_meta rich_media_meta_text"]/text()').extract())
                Author = ''.join(meta_list.xpath('.//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()').extract())
                content_primary = selector.xpath('.//div[@class="rich_media_content "]')
                content_p = ''.join(content_primary.xpath('.//text()').extract()).strip()
                #注意，这里获取img链接的时候，要用 data-src
                content_img = '---'.join(content_primary.xpath('.//p//img/@data-src').extract())

                item = TigerItem()
                item['Url'] = response.url
                item['Title'] = title
                item['Date'] = date
                item['Author'] = Author
                item['Source'] = 'weixin'
                item['Img'] = content_img
                item['Content'] = content_p
                yield item