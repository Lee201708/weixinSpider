from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from urllib.request import urlopen
import requests
import time
import socket


class GetIP(CrawlSpider):
    name = 'IPSpider'

    start_urls = [
        'http://www.xicidaili.com/'
    ]
    # url ='http://www.baidu.com'
    url ='http://ip.chinaz.com/getip.aspx'
    def parse(self,response):
        # print(response.body)
        # socket.setdefaulttimeout(3)
        selector = Selector(response)
        main = selector.xpath('body/div[@id="wrapper"]/div[@id="body"]/div[@id="home"]/div[@class="main"]')
        tr = main.xpath('.//table/tr[position() >2 and position() < 23]')
        ips = tr.xpath('.//td[2]/text()').extract()
        ports = tr.xpath('.//td[3]/text()').extract()
        try:
            self.file = open('IPPOOL.txt', 'w', encoding='utf-8')
            for i in range(0,len(ips)):
                # time.sleep(0.5)
                proxy_host = "http://" + ips[i] + ':' + ports[i]
                # try:
                #     r = requests.get(url=self.url, proxies={"http":proxy_host})
                #     if r.status_code == 200:
                #         print('success:', proxy_host)
                #     else:
                #         print('没用的代理', proxy_host)
                # except BaseException as e:
                #     print('error PROXY:',proxy_host)
                #     pass
                self.file.write(proxy_host + '\n')
                print('写入成功')
        finally:
            self.file.close()
    #
    # def validateIp(proxy):
    #     url = "http://ip.chinaz.com/getip.aspx"
    #     f = open("ip.txt", "w")
    #     socket.setdefaulttimeout(3)
    #     for i in range(0, len(proxy)):
    #         try:
    #             ip = proxy[i].strip().split("\t")
    #             proxy_host = "http://" + ip[0] + ":" + ip[1]
    #             proxy_temp = {"http": proxy_host}
    #             res = urlopen(url, proxies=proxy_temp).read()
    #             f.write(proxy[i] + '\n')
    #             print
    #             proxy[i]
    #         except BaseException as  e:
    #             continue
    #     f.close()

                    #
    # def detect(self):
    #     '''
    #     http://ip.chinaz.com/getip.aspx  作为检测目标
    #     :return:
    #     '''
    #     # proxys = self.db_helper.proxys.find()
    #
    #     badNum = 0
    #     goodNum = 0
    #     for proxy in proxys:
    #         ip = proxy['ip']
    #         port = proxy['port']
    #         try:
    #             proxy_host = "http://" + ip + ':' + port  #
    #             response = urllib.urlopen(self.url, proxies={"http": proxy_host})
    #             if response.getcode() != 200:
    #                 self.db_helper.delete({'ip': ip, 'port': port})
    #                 badNum += 1
    #                 print
    #                 proxy_host, 'bad proxy'
    #             else:
    #                 goodNum += 1
    #                 print
    #                 proxy_host, 'success proxy'
    #
    #         except Exception, e:
    #             print
    #             proxy_host, 'bad proxy'
    #             self.db_helper.delete({'ip': ip, 'port': port})
    #             badNum += 1
    #             continue
    #
    #     print('success proxy num : ', goodNum)
    #     print('bad proxy num : ', badNum)