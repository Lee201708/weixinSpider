# -*- coding: utf-8 -*-

import requests
import socket
from urllib.request import urlopen


class testIP(object):
    url = 'http://www.baidu.com'
    # url = 'http://ip.chinaz.com/getip.aspx'

    def getIP(self):
        IP = []
        try:
            self.file = open('IPPOOL.txt','r',encoding='utf-8')
            for i in self.file:
                IP.append(i)
            return IP
        except:
            print('something wrong!attention')
            return IP


    def testIP(self,IP):
        socket.setdefaulttimeout(3)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        for ip in IP:
            try:
                res = requests.get(url=self.url, headers=headers,timeout=10,proxies={"http":ip})
                # proxy_temp = {"http": ip}
                # res = urlopen(self.url, proxies=proxy_temp).read()
                if res.status_code == 200:
                    result = 'success:'+ ip
                else:
                    result = 'false:' + ip
            except BaseException as e:
                result = 'error PROXY:'+ip
            finally:
                print(result)

    def testIP2(self):
        self.file = open('IPPOOL.txt', 'r', encoding='utf-8')
        for ip in self.file:
            try:
                r = requests.get(url=self.url, proxies={"http":ip})
                if r.status_code == 200:
                    result = 'success:'+ ip
                else:
                    result = 'false:' + ip
                    return result
            except BaseException as e:
                result = 'error PROXY:'+ip
                return result
                pass


if __name__ == '__main__':
    test = testIP()
    ipList = test.getIP()
    test.testIP(ipList)

