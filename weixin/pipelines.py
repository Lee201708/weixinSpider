'''
创建日期：2017.4.17
创建人：Lee
功能：最终的数据处理。  去重并将链接存入 redis

'''
# -*- coding: utf-8 -*-
import json
from weixin.items import NewsItem
from scrapy.utils.project import get_project_settings
import redis
from scrapy.exceptions import DropItem
import time
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import time




now = time.strftime("%Y%m%d")
setting = get_project_settings()
HOST = setting.get('REDIS_HOST')
PORT = setting.get('REDIS_PORT')
# DB = setting.get('REDIS_DB')
try:
    r = redis.Redis(HOST, PORT)
except Exception as e:
    print(e)
    print('redis连接失败！')

class WeixinPipeline(object):
    def process_item(self, item, spider):
        return item

# class RedisPushPipeline(object):
#
#     def process_item(self,item,spider):
#         if isinstance(item,NewsItem):
#             url = item['Url']
#             self.r.lpush('wxNews:start_urls',url)
#         return item

class DupelicatePipeline_HotWord(object):

    def open_spider(self,spider):
        self.count = 1              #热词总数
        self.insertCount = 1        #成功插入的热词数
        self.dupeConut = 1          #重复的热词数

    def process_item(self, item, spider):
        hotword = item['HotWord']
        self.count += 1
        if r.sadd('HotWord:dupefilter',hotword):
            self.insertCount += 1
            print('插入成功！')
            BDurl = item['BDHotWordLink']
            WXurl = item['WXHotWordLink']
            r.lpush('BDNews:urls',BDurl)
            r.lpush('WXNews:urls',WXurl)
            # self.r.lpush('wx:urls')
            return item
        else:
            print('插入失败！')
            self.dupeConut += 1
            raise DropItem("Duplicate item found: %s" % item)

    def close_spider(self,spider):
        print('共有 %d 条热词' % self.count)
        print('成功插入 %d 条热词' % self.insertCount)
        print('共有 %d 条重复' % self.dupeConut)
        #当网络错误或代码错误，搜到的热词总数为0时，重复数也为0，这时应该增加再次搜索的时间，以期待管理人员发现错误之前，减少网络访问。
        if self.dupeConut > 500 or self.count == 0:
            with open('IncreaseTime.txt','w') as IT:
                word = 'True'
                IT.write(word)
                IT.close()
        else:
            with open('IncreaseTime.txt', 'w') as IT:
                word = 'False'
                IT.write(word)
                IT.close()
        self.count = 0
        self.dupeConut = 0
        self.insertCount = 0

class DupelicatePipeline_News(object):

    # spider启动信号和spider_opened函数绑定
    def __init__(self):
        dispatcher.connect(self.spider_idle, signals.spider_idle)


    def open_spider(self,spider):
        self.outlet = True          # 判断是否已经输出过 插入信息（避免idle函数重复执行）
        self.count = 0              #新闻链接总数
        self.insertCount = 0        #成功插入的新闻链接数
        self.dupeConut = 0          #重复的新闻链接数v

    def process_item(self, item, spider):
        self.outlet = True
        url = item['TitleLink']
        self.count += 1
        if r.sadd('Media:dupefilter',url):
            self.insertCount += 1
            print('插入成功！')
            r.lpush('WXMedia:urls',url)
            return item
        else:
            print('插入失败！')
            self.dupeConut += 1
            raise DropItem("Duplicate item found: %s" % item['Title'])
        #
        # if self.r.exists('url:%s' % url):
        #     self.dupeConut += 1
        #     print('重复------------------ : %s' % url)
        #     raise DropItem("Duplicate item found: %s" % item)
        #
        # else:
        #     self.r.set('url:%s' % url, 1)
        #     return item
    #当爬虫空闲时调用 idle函数
    def spider_idle(self,spider):
        time.sleep(1)
        if self.outlet:
            print('共有 %d 条新闻链接' % self.count)
            print('成功插入 %d 条新闻链接' % self.insertCount)
            print('共有 %d 条重复' % self.dupeConut)
            self.outlet = False
        else:
            pass

    def close_spider(self,spider):
        print('共有 %d 条新闻链接' % self.count)
        print('成功插入 %d 条新闻链接' % self.insertCount)
        print('共有 %d 条重复' % self.dupeConut)
        self.count = 0
        self.dupeConut = 0
        self.insertCount = 0



#写入json文件
class JsonWritePipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_idle, signals.spider_idle)
        # self.opened = True

    def open_spider(self, spider):
        self.opened = True
        self.file = open('json/'+spider.name+now+'.json', 'a+', encoding='utf-8')
        print('json file is open!')

    def process_item(self, item, spider):
        if not self.opened:
            now = time.strftime("%Y%m%d")
            self.file = open('json/' + spider.name + now + '.json', 'a+', encoding='utf-8')
            print('json file is open again!')
            self.opened = True
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_idle(self):
        if self.opened:
            time.sleep(3)
            self.opened = False
            self.file.close()
            print('json file is closed!')
        else:
            pass

    def spider_closed(self):
        if self.opened:
            self.file.close()
        else:
            pass


class JsonWritePipeline_HotWordSpider(object):
    # def __init__(self):
    #     self.file = codecs.open('cnblogs.json', 'w', encoding='utf-8')
    def open_spider(self, spider):
        self.file = open('json/HotWordSpider'+now+'.json','a+',encoding='utf-8')

    def process_item(self, item, spider):
        #ebsure_ascii = False 确保输出的中文，而不是ascii字符码
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

class JsonWritePipeline_NewsSpider(object):
    def open_spider(self,spider):
        self.file = open('json/NewsSpider'+now+'.json','a+',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self):
        self.file.close()

    # def spider_idle(self,spider):
    #     print('i am free')

class JsonWritePipeline_MediaSpider(object):
    def open_spider(self, spider):
        self.file = open('json/MediaSpider'+now+'.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self):
        self.file.close()
