'''
author：Lee
功能：使用selenium打开无界面浏览器Phantom，截取验证码图片保存到本地。
      输入验证码并获取验证成功后的cookie

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from pyquery import PyQuery as pq
from time import sleep
from PIL import Image
from transCookie import transCookie
import PIL
import urllib
from urllib import request

class killYanZhengMa(object):
    def __init__(self):
        # self.browser = webdriver.Chrome()
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3) # 隐性等待，最长等30秒
        self.wait = WebDriverWait(self.browser,10)
        self.browser.set_window_size(1100, 700)

    def getCookie(self):
        try :
            self.browser.get('http://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d2%26query%3d%E6%9E%97%E5%85%81%E5%84%BF%26ie%3dutf8%26s_from%3dinput%26_sug_%3dy%26_sug_type_%3d1%26w%3d01015002%26oq%3d%26ri%3d66%26sourceid%3dsugg%26sut%3d0%26sst0%3d1495180156590%26lkt%3d0%2C0%2C0%26p%3d40040108')
            # pic = wait.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR,'#seccodeInput'))
            # )
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#seccodeInput')))
            self.browser.get_screenshot_as_file("screen.png")
            img = Image.open("screen.png")
            region = (450, 252, 548, 290)
            # 裁切图片
            cropImg = img.crop(region)
            # 保存裁切后的图片
            try:
                cropImg.save('crop.jpg')
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit'))
                )
                inputer = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#seccodeInput'))
                )
                inputer.send_keys(input('请输入验证码'))
                submit.click()
                sleep(1)
                try:
                    print('正在验证验证码')
                    # errorTips = EC.presence_of_element_located((By.CSS_SELECTOR,'#error-tips'))
                    html = self.browser.page_source
                    doc = pq(html)
                    errorTips = doc('#error-tips').text()
                    if errorTips:
                        print('验证码输入错误，请等待重新输入')
                        # self.browser.close()
                        self.getCookie()
                    else:
                        print('验证成功！')
                        # get the session cookie
                        # print("未处理",self.browser.get_cookies())
                        # print(self.browser.get_cookies())
                        cookie = [item["name"] + "=" + item["value"] for item in self.browser.get_cookies()]
                        # print(cookie)
                        cookiestr = ';'.join(item for item in cookie)
                        cookies = transCookie(cookiestr).stringToDict()
                        # print(cookiestr)
                        # print("已处理",cookies)
                        self.browser.close()
                        return cookies
                except Exception as e:
                    print("出现错误%s"%e)
            except IOError as e:
                print('保存图片失败，显示错误信息%s'%e)
        except TimeoutException as e:
            print('访问超时：%s'%e)
            self.getCookie()


    # def get_src():
    #     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#seccodeInput')))
    #     html = browser.page_source
    #     doc = pq(html)
    #     Src = doc('#seccodeImage').attr('src')
    #     imgSrc = 'http://weixin.sogou.com/antispider/%s'%Src
    #     print(imgSrc)
    #     return imgSrc

    # def save_img(url):
    #     # tamp = str(int(time.time() * 10))
    #     # url = 'http://weixin.sogou.com/antispider/util/seccode.php?tc=%s'%tamp
    #     try:
    #         urllib.request.urlretrieve(url, 'check.jpg')
    #         print('图片下载完成')
    #         return True
    #     except Exception as e:
    #         print('下载图片出现错误',e)
    #         return False

'''weixinIndexVisited=1; SUID=8CBE913D771A910A0000000058DDA6CD; IPLOC=CN4419;
SUV=1492158383483625; CXID=B63EA330BDD8F2D9534ADD9533FAC6F4; pgv_pvi=4474822656;
ABTEST=2|1494817082|v1; sw_uuid=6015393082; sg_uuid=3157350693; ssuid=8053006356;
dt_ssuid=6644722780; cd=1495070098&0d0108596e7f2b5f188360272421ad08;
rd=4lllllllll2YDwZfQS8C6O6tdYiB45Qv5BpM0lllll9llllx9A7ll5@@@@@@@@@@;
JSESSIONID=aaaBkQHXvadHB6kSBT2Vv; PHPSESSID=c1prfrgupvb86a2k1v5ujm5q66;
ld=hlllllllll2YDwZfQS8C6O6WOvqB45Qv5BpM0lllll9lllll9h7ll5@@@@@@@@@@;
LSTMV=214%2C263; LCLKINT=1821; sct=121; SNUID=10220DA19B9ECCBD4449549F9CA8F261;
wuid=AAEKPeHqGAAAAAqLE2MuMgIAIAY=; ad=wkllllllll2Y@U@blllllV60dNtlllll5BpM0llllxklllllVCxlw@@@@@@@@@@@;
SUID=8CBE913D4C238B0A58AF87C60008873A; SUIR=10220DA19B9ECCBD4449549F9CA8F261; seccodeRight=success; successCount=2|Wed, 24 May 2017 05:45:33 GMT'''


if __name__ == '__main__':
    way = killYanZhengMa()
    # way.search()
    way.getCookie()