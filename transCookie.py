# @author   Lee
# @date     2017.08.16
# @DO       调整cookie格式




class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    # cookie = "weixinIndexVisited=1; SUID=8CBE913D771A910A0000000058DDA6CD; IPLOC=CN4419; SUV=1492158383483625; CXID=B63EA330BDD8F2D9534ADD9533FAC6F4; pgv_pvi=4474822656; SUID=8CBE913D4C238B0A58AF87C60008873A; ABTEST=2|1494817082|v1; SNUID=7A4866CAF7F2B971CFC13C1CF7513C1C; clientId=3CE4AB923EA069D91DF0A1EE3F016802; ad=eZllllllll2Y@U@blllllV6zzkZlllll5BpM0lllllwlllll9Vxlw@@@@@@@@@@@; JSESSIONID=aaajGpAhcojEEfW-UW2Vv; PHPSESSID=dn0l71e6r3mtdls8122qaas694; SUIR=7A4866CAF7F2B971CFC13C1CF7513C1C; ld=Slllllllll2YDwZflllllV6bIPklllll5BpM0lllllGlllll9v7ll5@@@@@@@@@@; LSTMV=314%2C207; LCLKINT=6972; sw_uuid=6015393082; sg_uuid=3157350693; ssuid=8053006356; dt_ssuid=6644722780; sct=86"
    # print(cookie)
    # cookie = "weixinIndexVisited=1; SUID=8CBE913D771A910A0000000058DDA6CD; IPLOC=CN4419; SUV=1492158383483625; CXID=B63EA330BDD8F2D9534ADD9533FAC6F4; pgv_pvi=4474822656; ABTEST=2|1494817082|v1; SUIR=7A4866CAF7F2B971CFC13C1CF7513C1C; sw_uuid=6015393082; sg_uuid=3157350693; ssuid=8053006356; dt_ssuid=6644722780; LSTMV=278%2C180; LCLKINT=3650; ld=4lllllllll2YDwZfQS8C6O6tdYiB45Qv5BpM0lllll9llllx9A7ll5@@@@@@@@@@; cd=1495070098&0d0108596e7f2b5f188360272421ad08; rd=4lllllllll2YDwZfQS8C6O6tdYiB45Qv5BpM0lllll9llllx9A7ll5@@@@@@@@@@; JSESSIONID=aaaBkQHXvadHB6kSBT2Vv; ad=olllllllll2Y@U@blllllV6W5T7lllll5BpM0lllllYlllll9Cxlw@@@@@@@@@@@; SUID=8CBE913D4C238B0A58AF87C60008873A; SNUID=D7E2CD665B5E148A45A8B5175C546167; PHPSESSID=c1prfrgupvb86a2k1v5ujm5q66; sct=114; refresh=1; seccodeRight=success; successCount=1|Fri, 19 May 2017 03:03:59 GMT"
    cookie = 'ABTEST=1|1495607669|v1; IPLOC=CN4419; SUID=8CBE913D2423910A0000000059252975; PHPSESSID=6so53buv1i9e4kc4mqcbsljhi6; SUIR=1495607669; SUID=8CBE913D3320910A0000000059252975; SUV=007E53963D91BE8C5925297554C3E154; SNUID=61537FD0EDE8BED2A20569A7EE9E22B0; seccodeRight=success; successCount=1|Wed, 24 May 2017 06:37:15 GMT; refresh=1; JSESSIONID=aaaW4CLriQu4xck1rGFWv'
    trans = transCookie(cookie)
    print(trans.stringToDict())