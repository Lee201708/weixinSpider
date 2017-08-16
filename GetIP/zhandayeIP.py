'''
创建日期：2017.1.14
创建人：Lee
功能：获取 “站大爷” 代理ip

'''


import requests
import re
from lxml import etree
from multiprocessing.dummy import Pool
import json




headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }


def getIP():

    url = 'http://ip.zdaye.com/dayProxy/ip/1152.html'
    html = requests.get(url,headers).content
    ipList = list()
    # print(html)
    selector = etree.HTML(html)
    content = selector.xpath('//body/div[@class="container mt40"]/div[@class="container mt40"]')[0]
    content2 = content.xpath('.//div[@class="col-md-9"]/div[@class="row"]/div/div[@class="panel panel-success"]/div[@class="panel-body"]/div[@class="row"]//div[@class="cont"]//text()')
    # file = open('zhandayeProxy.txt', 'w',encoding='utf-8')
    for i in content2:
        pro = 'http://%s'%i
        # file.write('http://%s\n' % i )
        ipList.append(pro)
        # print(i, '存储成功')
    return ipList

def test(ip):
    url = 'http://www.baidu.com'
    # for ip in ipList:
    IPList = []
    try:
        # print(ip)
        res = requests.get(url=url, headers=headers, timeout=10, proxies={"http": ip})
        # proxy_temp = {"http": ip}
        # res = urlopen(self.url, proxies=proxy_temp).read()
        if res.status_code == 200:
            result = 'success:' + ip

            print(result)
            IPList.append(ip)
        else:
            result = 'false:' + ip
            print(result)
    except BaseException as e:
        result = 'error PROXY:' + ip
        print(result)
    return IPList

def mulTestProxies(init_proxies):
    '''
    功能：多进程验证IP有效性
    @init_proxies：原始未验证代理IP池
    '''
    pool = Pool(processes=4)
    pool.map(test,init_proxies)
    pool.close()
    pool.join()  #等待进程池中的worker进程执行完毕


if __name__ == '__main__':
    ipList = getIP()
    #-------------------
    mulTestProxies(ipList)


    # for ip in ipList:
    #     ipList_useful = test(ip)
     #-------------------
