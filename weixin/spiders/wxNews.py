'''
创建日期：2017.4.17
创建人：Lee
功能：从新闻列表页获取所有的新闻标题和新闻链接

'''

from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request,FormRequest
from urllib.parse import urlencode
from scrapy.selector import Selector
from weixin.items import NewsItem
import redis
from scrapy.utils.project import get_project_settings
import re
import logging
from urllib.parse import unquote
import time
from urllib.request import urlretrieve
import urllib
class wxNews(RedisSpider):

    name = 'wxNewsSpider'
    # logging.basicConfig(filename='logs/WXNewsSpiderInfologger.log', level=logging.INFO)
    custom_settings = {
        'ITEM_PIPELINES' : {
            'weixin.pipelines.JsonWritePipeline': 400,
            'weixin.pipelines.DupelicatePipeline_News': 200,
        },
        'DEFAULT_REQUEST_HEADERS' : {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://weixin.sogou.com/'
        }
    }
    times = 0
    redis_key = 'WXNews:urls'
    # start_urls = [
    #     'http://weixin.sogou.com/'
    # ]

    # def start_requests(self):
    #     params = {
    #         'type': '2',
    #         'query': '惠英红三夺影后',
    #         'ie': 'utf8',
    #         's_from': 'input',
    #         '_sug_': 'n',
    #         '_sug_type_': ''
    #     }
    #     param = urlencode(params)
    #     urls = 'weixin?'.join(['http://weixin.sogou.com/',param])
    #     #控制页数
    #     for i in range(1,3):
    #         url = urls + '&page=%d'%i
    #         yield Request(url=url,callback=self.parse_item)

    # def start_requests(self):
    #     url = 'http://www.jycinema.com/frontUIWebapp/appserver/cinCinemaFilmViewService/findFilm'
    #     form_data = {
    #         'params': '''{"type":"queryFilm","cityName":"深圳市","cinemaId":"","statusRE":"RELEASE","channelCode":"J0002","channelId":"3"}'''
    #     }
    #     return [scrapy.FormRequest(url, formdata=form_data, headers=self.headers, callback=self.parse_item)]



    #备选，如果只能在redis中存储已经处理过的url的话
    def parse(self,response):
        urls = response.url
        if None:
            pass
        #如果出现验证码，则在此开始
        # bossurl = 'http://weixin.sogou.com/antispider/thank.php'
        # found = urls.find('antispider')
        # if found > 0 and urls != bossurl:
        #     input('大哥，快点去浏览器输入验证码，然后回来按个确认，等着干活呢')
        # tamp = str(int(time.time() * 10))
        # url = 'http://weixin.sogou.com/antispider/util/seccode.php?tc=%s'%tamp
        # bossurl = 'http://weixin.sogou.com/antispider/thank.php'
        # urllib.request.urlretrieve(url, 'check.jpg')
        # # file = open('chekc.jpg','wb+')
        # # file.write()
        # word= input('请输入验证码：')
        # fm = re.findall('http://weixin\.sogou\.com/antispider/\?from=(.*?)',urls)
        # print('输入验证码以后')
        # yield (FormRequest(bossurl,
        #         formdata={
        #             'c':word,
        #             'r':fm,
        #             'v':'1'
        #         },
        #         callback=self.parse
        #                                   ))
        #网页正常浏览
        else:
            self.parse_item(response)
            for i in range(2,4):
                time.sleep(1)
                url = urls +  '&page=%d'%i
                yield Request(url,callback=self.parse_item)

    def parse_item(self,response):
        if self.times >200:
            time.sleep(20)
            print("已处理200条，将暂停20秒")
            self.times = 0
        self.times += 1
        responseUrl = response.url
        '''http://weixin.sogou.com/weixin?type=2&query=%E6%83%A0%E8%8B%B1%E7%BA%A2%E4%B8%89%E5%A4%BA%E5%BD%B1%E5%90%8E&ie=utf8&s_from=input&_sug_=n&_sug_type_=&page=1'''
        words = re.findall('.*?query=(.*?)&ie=utf8.*?',responseUrl)
        if words ==[]:
            print('WARMING!错误链接%s'%response.request.url)
            print(response.status)
            return
        else:
            word = unquote(words[0])
            selector = Selector(response)
            item = NewsItem()
            News_Box = selector.xpath('.//div[@class="news-box"]')
            News_list = News_Box.xpath('ul[@class="news-list"]')
            News_contents = News_list.xpath('li/div[@class="txt-box"]')
            for News_content in News_contents:
                # title =''.join(News_content.xpath('h3/a//text()').extract_unquoted()
                title = ''.join(News_content.xpath('h3/a//text()').extract())
                url = News_content.xpath('h3/a/@href').extract()[0]
                summary = ''.join(News_content.xpath('p//text()') .extract())
                item['FromWord'] = word
                item['Title'] = title
                item['TitleLink'] = url
                item['Summary'] = summary
                yield item

