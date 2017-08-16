'''
创建日期：2017.4.17
创建人：Lee
功能：下载中间件。 设置随机User-Agent ，随机代理

'''

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy import log
from weixin.settings import IPPOOL
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
import base64
import json
from seleni import *


class WeixinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.count = 0
        self.agents = agents
        # self.cooki = {'weixinIndexVisited': '1', 'SUID': '8CBE913D4C238B0A58AF87C60008873A', 'IPLOC': 'CN4419', 'SUV': '1492158383483625', 'CXID': 'B63EA330BDD8F2D9534ADD9533FAC6F4', 'pgv_pvi': '4474822656', 'ABTEST': '2|1494817082|v1', 'SUIR': '7A4866CAF7F2B971CFC13C1CF7513C1C', 'sw_uuid': '6015393082', 'sg_uuid': '3157350693', 'ssuid': '8053006356', 'dt_ssuid': '6644722780', 'LSTMV': '278%2C180', 'LCLKINT': '3650', 'ld': '4lllllllll2YDwZfQS8C6O6tdYiB45Qv5BpM0lllll9llllx9A7ll5@@@@@@@@@@', 'cd': '1495070098&0d0108596e7f2b5f188360272421ad08', 'rd': '4lllllllll2YDwZfQS8C6O6tdYiB45Qv5BpM0lllll9llllx9A7ll5@@@@@@@@@@', 'JSESSIONID': 'aaaBkQHXvadHB6kSBT2Vv', 'ad': 'olllllllll2Y@U@blllllV6W5T7lllll5BpM0lllllYlllll9Cxlw@@@@@@@@@@@', 'SNUID': 'D7E2CD665B5E148A45A8B5175C546167', 'PHPSESSID': 'c1prfrgupvb86a2k1v5ujm5q66', 'sct': '114', 'refresh': '1', 'seccodeRight': 'success', 'successCount': '1|Fri, 19 May 2017 03:03:59 GMT'}
        self.cooki = {'SUID': '8CBE913D3220910A0000000059252F45', 'ABTEST': '8|1495609157|v1', 'SUIR': '1495609157', 'IPLOC': 'CN4419', 'PHPSESSID': '6nvs796ob3s3d7mvar0486eo32', 'SNUID': '61537CD0ECE8BDD2409F6A25EDDCF7C1', 'seccodeRight': 'success', 'SUV': '008C01EF3D91BE8C59252F45AFEA2750', 'successCount': '1|Wed, 24 May 2017 07:04:15 GMT', 'refresh': '1', 'JSESSIONID': 'aaaySvfBjRlOP56BDEFWv'}


    # def spider_opened(self,spider):
    #     print('hello,i am from middleware.open_spider---------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # 从crawler构造，USER_AGENTS定义在crawler的配置的设置中

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.settings.getlist('USER_AGENTS'))
    #
    # # 从settings构造，USER_AGENTS定义在settings.py中
    @classmethod
    def from_settings(cls, settings):
        return cls(settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))
        request.headers.setdefault('Accept',
                                   'text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.headers.setdefault('Connection', 'keep-alive')
        request.headers.setdefault('Upgrade-Insecure-Requests', '1')
        request.headers.setdefault('Accept-Encoding', 'gzip,deflate,sdch')
        request.headers.setdefault('Cache-Control', 'max-age=0')
        # request.headers.setdefault('Accept-Language','zh-CN,zh;q:0.8')
        if spider.name == 'wxNewsSpider':
            request.headers.setdefault('Referer','http://weixin.sogou.com/')
            request.headers.setdefault('Host','weixin.sogou.com')
            # request.headers.setdefault('Accept-EncodingCookie',"{'weixinIndexVisited': '1', 'SUID': '8CBE913D4C238B0A58AF87C60008873A', 'IPLOC': 'CN4419', 'SUV': '1492158383483625', 'CXID': 'B63EA330BDD8F2D9534ADD9533FAC6F4', 'pgv_pvi': '4474822656', 'ABTEST': '2|1494817082|v1', 'SNUID': '7A4866CAF7F2B971CFC13C1CF7513C1C', 'clientId': '3CE4AB923EA069D91DF0A1EE3F016802', 'ad': 'eZllllllll2Y@U@blllllV6zzkZlllll5BpM0lllllwlllll9Vxlw@@@@@@@@@@@', 'JSESSIONID': 'aaajGpAhcojEEfW-UW2Vv', 'PHPSESSID': 'dn0l71e6r3mtdls8122qaas694', 'SUIR': '7A4866CAF7F2B971CFC13C1CF7513C1C', 'ld': 'Slllllllll2YDwZflllllV6bIPklllll5BpM0lllllGlllll9v7ll5@@@@@@@@@@', 'LSTMV': '314%2C207', 'LCLKINT': '6972', 'sw_uuid': '6015393082', 'sg_uuid': '3157350693', 'ssuid': '8053006356', 'dt_ssuid': '6644722780', 'sct': '86'}")
            request.cookies = self.cooki
            # print('这是原始的cookie', request.cookies)
            # request.cookies = {'ABTEST': '1|1495607669|v1', 'IPLOC': 'CN4419', 'SUID': '8CBE913D3320910A0000000059252975', 'PHPSESSID': '6so53buv1i9e4kc4mqcbsljhi6', 'SUIR': '1495607669', 'SUV': '007E53963D91BE8C5925297554C3E154', 'SNUID': '61537FD0EDE8BED2A20569A7EE9E22B0', 'seccodeRight': 'success', 'successCount': '1|Wed, 24 May 2017 06:37:15 GMT', 'refresh': '1', 'JSESSIONID': 'aaaW4CLriQu4xck1rGFWv'}
        elif spider.name == 'wxMediaSpider':
            request.headers.setdefault('Referer', 'http://weixin.sogou.com/')
            request.headers.setdefault('Host', 'mp.weixin.qq.com')
        # log.msg('>>>> UA %s' % request.headers)

    def process_response(self, request, response, spider):
        # log.msg('>>>> response.status %s' % response.status)
        # print("-------------------", response.status, "-----------------------")
        # # print('cookies', request.cookies)
        # print(response.url)
        # print('这是原始的cookie',request.cookies)
        found = response.url.find("antispider")
        if found > 0 :
            KYZM = killYanZhengMa()
            cookies = KYZM.getCookie()
            self.cooki = cookies
            request.meta['cookiejar'] = self.cooki

            # print('这是新的cookie', request.cookies)
            # input('大哥，快点去浏览器输入验证码，然后回来按个确认，等着干活呢')
            return request
        # if (response.status == 200 and found < 0):
        #     self.count += 1
        # else:
        #     print(response.url)
        #     print('到达错误数量：',self.count)
        #     # input("打断，等待处理")
        #     return request
        return response

class RandomIPPoolMiddleware(HttpProxyMiddleware):

    def __init__(self,ip=None):
        self.ip = ip

    def process_request(self, request, spider):
        this_ip = random.choice(IPPOOL)
        try:
            request.meta['proxy'] = 'http://' + this_ip
            print('当前使用的IP是：', this_ip)
        except BaseException as e:
            print(e)
            pass

    def process_response(self,request,response,spider):
        print("-------------------",  response.status , "-----------------------")
        found = response.url.find("antispider")
        if(response.status != 200 or found > 0):
            print(request.meta['proxy'],'proxy错误')
            ip = random.choice(IPPOOL)
            request.meta['proxy'] = ip
            return request
        return response






#阿布云
class ProxyMiddleware(object):
    # 代理服务器
    proxyServer = "http://proxy.abuyun.com:9010"

    # 代理隧道验证信息
    proxyUser = "HF1164W4MR48F87P"
    proxyPass = "EA07850AA918EB92"

    # for Python2
    # proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

    # for Python3
    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

    def open_spider(self,spider):
        self.file = open('json/'+spider.name+'.json','a',encoding='utf-8')

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth
        line = json.dumps(self.proxyServer, ensure_ascii=False) + '\n'
        print(self.proxyServer)
        # self.file.write(line)

    def close_spider(self,spider):
        self.file.close()

