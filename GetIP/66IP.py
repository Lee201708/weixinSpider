'''
创建日期：2017.1.14
创建人：Lee
功能：获取 “66ip” 代理ip
状态：网站不可访问

'''



import requests
import chardet
import re
import threading
import time
from multiprocessing.dummy import Pool



headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'm.66ip.cn'
            }
def save():
    ipList = list()
    url = ("http://m.66ip.cn/mo.php?tqsl={proxy_number}")
    url = url.format(proxy_number=10)
    html = requests.get(url, headers=headers).content
    html = html.decode(chardet.detect(html)['encoding'])
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
    all_ip = re.findall(pattern, html)
    for i in all_ip:
        ipList.append('http://'+i)
    return ipList
    # print(all_ip)

    # file = open('66IP.txt','w',encoding='UTF-8')
    # for i in all_ip:
    #     file.write('http://' + i + '\n')
    # file.close()

def test(ip):
    url = 'http://www.baidu.com'
    # for ip in ipList:
    IPList = []
    try:
        print(ip)
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
    finally:
        return IPList



def mulTestProxies(init_proxies):
    '''
    功能：多进程验证IP有效性
    @init_proxies：原始未验证代理IP池
    '''
    pool = Pool(processes=4)
    fl_proxies = pool.map(test,init_proxies)
    pool.close()
    pool.join()  #等待进程池中的worker进程执行完毕
    return fl_proxies

if __name__ == '__main__':
    # IPlist = list()
    IPlist = save()
    print(IPlist)
    # t1 = time.strftime('%H-%M-%S')
    # mulTestProxies(IPlist)
    # # pool = Pool(2)
    # # pool.map(test,IPlist)
    # # for i in list:
    #     # t = threading.Thread(target=test,args=[i])
    #     # t.start()
    # t2 = time.strftime('%H-%M-%S')
    # print(t1,t2)

    tmp_proxies = mulTestProxies(IPlist)  # 多进程测试原始代理IP
    proxy_addrs = []
    for tmp_proxy in tmp_proxies:
        if len(tmp_proxy) != 0:
            proxy_addrs.append(tmp_proxy)
    print(proxy_addrs)












































#
# from multiprocessing import Process
# import threading
# import time
#
# lock = threading.Lock()
#
#
# def run(info_list, n):
#     lock.acquire()
#     info_list.append(n)
#     lock.release()
#     print('%s\n' % info_list)
#
#
# info = []
#
# for i in range(10):
#     '''target为子进程执行的函数，args为需要给函数传递的参数'''
#     p = Process(target=run, args=[info, i])
#     p.start()
#
# '''这里是为了输出整齐让主进程的执行等一下子进程'''
# # time.sleep(1)
# print('------------threading--------------')
#
# for i in range(10):
#     p = threading.Thread(target=run, args=[info, i])
#     p.start()












