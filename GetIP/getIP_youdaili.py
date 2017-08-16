import requests
import re

def getIP():
    of = open('YouDaiLiProxy.txt', 'w')
    url = 'http://www.youdaili.net/Daili/http/36723.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    # for i in range(1, 4):
    #     if i == 1:
    #         Url = url + '.html'
    #     else:
    #         Url = url + '_%s.html' % i
    html = requests.get(url,headers).text
    print(html)
    res = re.findall(r'\d+\.\d+\.\d+\.\d+\:\d+', html)
    for pro in res:
        of.write('http=%s\n' % pro)
        print(pro)
    of.close()

if __name__ == '__main__':
    getIP()
