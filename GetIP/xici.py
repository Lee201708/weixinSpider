import urllib.request
from bs4 import BeautifulSoup
import csv
from multiprocessing.dummy import Pool
from urllib.error import HTTPError
import threading
import socket
def IPspider():
    # IPpool = []
    file = open('xici.json','a')
    url = 'http://www.xicidaili.com/nn/'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
    header = {'User-agent': user_agent}
    for num in range(1, 5):
        ipurl = url + str(num)
        print('Now downloading the ' + str(num * 100) + ' ips')
        # request = urllib.Request(ipurl, headers=headers)
        # content = urllib2.urlopen(request).read()
        req = urllib.request.Request(ipurl,headers=header)
        response = urllib.request.urlopen(req,timeout=2000)
        resu = response.read()
        bs = BeautifulSoup(resu, 'html.parser')
        res = bs.find_all('tr')
        for item in res:
            try:
                tds = item.find_all('td')
                proxy = tds[1].text + ':' + tds[2].text
                # IPpool.append(proxy)
                file.write(proxy+'\n')
            except IndexError:
                pass
    file.close()

def IPpool(row):
    IPpool=[]
    user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
    header = {'User-agent': user_agent}

    # proxy_handler=urllib2.ProxyHandler({"http":proxy})
    # opener=urllib2.build_opener(proxy_handler)
    # urllib2.install_opener(opener)
    # req = urllib.request.Request('http://www.baidu.com', headers=header,)
    proxy_support = urllib.request.ProxyHandler({'http':row})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', user_agent)]
    urllib.request.install_opener(opener)
    # html = response.read().decode('utf-8')
    try:
        # html=urllib2.urlopen('http://www.baidu.com')
        # lock.acquire()  # 获得锁
        file = open('Useful.json','a')
        response = urllib.request.urlopen('http://weixin.sogou.com/',timeout=2000)
        # resu = response.read()
        print(response.code)
        # print(resu)
        print('it is success',row)
        file.write(row)
        # lock.release()  # 释放锁
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # IPpools = IPspider()
    # socket.setdefaulttimeout(5)  # 设置全局超时时间
    # pool = Pool(processes=10)
    # pool.map(IPpool, IPpools)
    # pool.close()
    # pool.join()
    # IPpool(IPpools)

    # 多线程验证

    with open('kuaidaili.json', 'r') as IPpools:
        all_thread = []
        for row in IPpools:
            IP = []
            IP.append(row)
            t = threading.Thread(target=IPpool,args=IP)
            all_thread.append(t)
            t.start()

        for t in all_thread:
            t.join(3)
