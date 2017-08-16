'''
创建日期：2017.4.17
创建人：Lee
功能：从微信热词榜获取关键词，并将链接拼接好分别存到 WXHotWordLink 和 BDHotWordLink，并在 pipeline 中lpush 到 redis 中。

'''


from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
import re
import urllib
from urllib.parse import urlencode
from weixin.items import HotWordItem
import time
import logging
# from scrapy import log
# from scrapy.utils.log import configure_logging


class HotWord(CrawlSpider):
    name = 'wxHotWordSpider'
    #LEVEL设了跟没设一样，搞不明白
    # logging.basicConfig(filename='logs/WXHotWordSpiderInfologger2.log', level=logging.INFO)
    custom_settings = {
        'ITEM_PIPELINES': {
            'weixin.pipelines.JsonWritePipeline': 400,
            'weixin.pipelines.DupelicatePipeline_HotWord': 200,
            # 'weixin.pipelines.WeixinPipeline': 200,
        }
    }

    url_prefix = 'http://top.sogou.com/'
    start_urls = [
        url_prefix+'hot/shishi_1.html',         #实时热点
        url_prefix+'hot/sevendsnews_1.html',    #七日热点
        url_prefix+'movie/all_1.html',          #电影
        url_prefix+'tvplay/all_1.html',         #电视剧
        url_prefix+'tvshow/all_1.html',         #综艺
        url_prefix+'animation/all_1.html',      #动漫
        url_prefix+'book/all_1.html',           #小说
        url_prefix+'song/newsong_1.html',       #音乐
        url_prefix+'game/all_1.html',           #游戏
        url_prefix+'auto/all_1.html',           #汽车
        url_prefix+'people/all_1.html',         #人物
    ]

    headers = {
        'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'IPLOC=CN4419; SNUID=47725DF1CCC987BD9066242FCC1B7CB0; SUID=8CBE913D3020910A0000000058E5A95F; SUV=002D73533D91BE8C58E5A9604DE24010; sct=2',
        'Host': 'top.sogou.com',
        'Upgrade-Insecure-Requests': 1
    }
    # http: // top.sogou.com / tvplay / all_1.html
    def start_requests(self):
        for url in self.start_urls:
            time.sleep(2)
            yield Request(url=url,headers=self.headers)

    '''处理第一页'''
    def parse(self, response):
        if response.url == 'http://www.sogou.com/docs/error.htm':
            print('WARMING!跳到了错误界面')
            return
        else:
            # print(response.body)
            # logging.error('这里启动了logger')
            selector = Selector(response)
            item = HotWordItem()
            tp = selector.xpath('head/title/text()').extract()[0]
            contant = selector.xpath('body/div[@class="contant"]')
            list  = contant.xpath('./div[@class="main"]/ul')
            list_title = list.xpath('./li/span[@class="s2"]/p[1]/a/text()').extract()
            if list_title != []:
                for title in list_title:
                    item['HotWord'] = title
                    item['HotWordType'] = tp
                    item['WXHotWordLink'] = self.WXFirstPageUrl(title, tp)
                    item['BDHotWordLink'] = self.BDFirstPageUrl(title, tp)
                    yield item
            else:
                print('未匹配到内容，请检查页面是否有内容、匹配规则是否正确。')
            page_list = contant.xpath('.//div[@class="main"]/div[@class="tag-box"]/a[position()>1 and position()<4]/@href').extract()
            pageUrl_prefix = re.findall('(http://top\.sogou\.com/.*?/).*?',response.url)[0]
            for page in page_list:
                url = pageUrl_prefix + page
                time.sleep(0.5)
                yield Request(url=url,headers=self.headers,callback=self.parse_TwoAndThree)

    '''处理第二页、第三页'''
    def parse_TwoAndThree(self,response):
        if response.url == 'http://www.sogou.com/docs/error.htm':
            print('WARMING!跳到了错误界面，发生错误的链接：%s'%response.request.url)
            return
        else:
            selector = Selector(response)
            item = HotWordItem()
            tp = selector.xpath('head/title/text()').extract()[0]
            contant = selector.xpath('body/div[@class="contant"]')
            list = contant.xpath('./div[@class="main"]/ul')
            list_title = list.xpath('./li/span[@class="s2"]/p[1]/a/text()').extract()
            if list_title != []:
                for title in list_title:
                    item['HotWord'] = title
                    item['HotWordType'] = tp
                    item['WXHotWordLink'] = self.WXFirstPageUrl(title, tp)
                    item['BDHotWordLink'] = self.BDFirstPageUrl(title, tp)
                    yield item
            else:
                print('未匹配到内容，请检查页面是否有内容、匹配规则是否正确。')



    def BDFirstPageUrl(self, keyword,tp):
        # word = quote(keyword)
        '''http://news.baidu.com/ns?word=%E5%AE%9C%E6%AD%A5%E5%87%BA%E8%A1%8C&tn=news&from=news&cl=2&rn=20&ct=1'''
        params = {
            "word": keyword,
            "tn": "news",
            "ct": "1",
            "from": "news",
            "cl": "2",
            "rn": "20",
            "tp": tp
        }
        params = urllib.parse.urlencode(params)
        add_s = ''.join([self.url_prefix, "/ns"])
        BDFirstPageUrl = "?".join([add_s, "%s"]) % params
        return BDFirstPageUrl


    def WXFirstPageUrl(self,keyword,tp):
        params = {
            'type': '2',
            'query': keyword,
            'ie': 'utf8',
            's_from': 'input',
            '_sug_': 'n',
            '_sug_type_': '',
            'tp':tp
        }
        param = urlencode(params)
        urls = 'weixin?'.join(['http://weixin.sogou.com/', param])
        return urls








