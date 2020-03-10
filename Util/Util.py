import datetime
import json
import logging
import os
import re
from logging import handlers

import requests


def getroomid(userid, roomnum):
    if userid is not None:
        print('start find the user ' + userid + '\'s room password...')
        usernewno = getusernewno(userid)
        # print(usernewno)
        # userinfo = getuserinfo(usernewno)
        # print('current_coin : ' + userinfo['data']['user_info']['current_coin'])
        # print('used_coin : ' + userinfo['data']['user_info']['used_coin'])
        # print('channel : ' + userinfo['data']['user_info']['channel'])
        roomnum = getroomnum(usernewno)
        # print(roomnum)
        roomid = searchroom(roomnum)
    elif roomnum is not None:
        print('start to find the room ' + roomnum + ' password...')
        roomid = searchroom(roomnum)
    return roomid


# userid->usernewno
def getusernewno(userid):
    url = "http://soagw.live.szcsckj.com/xllive.zbsearch.s/v1/Search.json"

    payload = "{'length':20,'key':'" + userid + "','page':1}"
    headers = {
        'Content-Type': "text/plain",
        'Connection': 'close',
        'Host': "soagw.live.szcsckj.com",
        'Accept-Encoding': "gzip, deflate",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    pat = '"uid":\"(\w+)'
    result = re.findall(pat, response.text)
    return result[0]


# usernewno->userinfo
def getuserinfo(usernewno):
    url = "http://soagw.live.szcsckj.com/xllive.zbuserservice.s/v1/GetUserinfo.json"

    payload = "{'touserid':'" + usernewno + "'}"
    headers = {
        'Content-Type': "text/plain",
        'Connection': 'close',
        'Host': "soagw.live.szcsckj.com",
        'Accept-Encoding': "gzip, deflate",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    r = json.loads(response.text)
    return r


# usernewno -> roomnum
def getroomnum(usernewno):
    url = "http://soagw.pw.szcsckj.com/xllive.service.pwroominfo/v1/GetUserRoom"
    querystring = {"userId": usernewno}
    headers = {
        'Accept': "*/*",
        'Connection': 'close',
        'Host': "soagw.pw.szcsckj.com",
        'Accept-Encoding': "gzip, deflate",
    }

    response = requests.request("POST", url, headers=headers, params=querystring)
    pat = '"roomNum":\"(\w+)'
    result = re.findall(pat, response.text)
    return result[0]


# roomnum -> roomid
def searchroom(room_num):
    url = "http://soagw.pw.szcsckj.com/xllive.pwroomsearch.s/v1/SearchRoom.json"

    payload = "{'page':0,'limit':20,'keyword':'" + room_num + "'}"
    headers = {
        'Content-Type': "text/plain",
        'Connection': 'close',
        'Accept': "*/*",
        'Host': "soagw.pw.szcsckj.com",
        'Accept-Encoding': "gzip, deflate"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    pat = '"roomId":\"(\w+)'
    result = re.findall(pat, response.text)
    return result[0]


# roomid->password
def checkpassword(room_id, password, proxy=None):
    try:
        url = "http://soagw.pw.szcsckj.com/xllive.service.pwroominfo/v1/CheckPasswd"

        payload = "{'room_id':'" + room_id + "','password':'" + password + "'}"
        headers = {
            'Content-Type': "text/plain",
            'Connection': 'close',
            'Accept': "*/*",
            'Host': "soagw.pw.szcsckj.com",
            'Accept-Encoding': "gzip, deflate"
        }

        if proxy:
            print(password + '--------' + proxy)
            response = requests.request("POST", url, data=payload, headers=headers,
                                        proxies={'http': proxy})
        else:
            response = requests.request("POST", url, data=payload, headers=headers)
    except Exception as e:
        print(type(e))
        print(e)
        response = None

    return response


def getproxies():
    import requests

    url = "http://www.89ip.cn/tqdl.html"

    querystring = {"num": "3000", "address": "", "kill_address": "", "port": "", "kill_port": "", "isp": ""}

    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "2bc16990-172f-4fb4-b9d7-ebdce107bcbc,031c70c1-2f5e-4c2e-ac1f-cba1b9b83ded",
        'Host': "www.89ip.cn",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': "yd_cookie=6751e96f-1296-4483f82c9962191e40be64e7a1b6aefa90ea",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    pat = '(\d.*?)<br>'
    result = re.findall(pat, response.text)
    return result


def getfollowlist():
    url = "http://biz.live.szcsckj.com/caller"

    querystring = {"a": "getFollowList", "alluser": "1", "c": "player", "limit": "20", "playerid": "775338585",
                   "start": "0", "type": "focus"}

    headers = {
        'Host': "biz.live.szcsckj.com",
        'Accept': "*/*",
        'Cookie': "guid=adc7bea471d5e3b6b4507fb76ab7669a; deviceid=adc7bea471d5e3b6b4507fb76ab7669a; userid=775338585; sessionid=cs001.CEC64B3E5655877D9B9F7EB3B1FCE418; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; appid=1027; sign=e13a273c7454e883f953cc706007815c; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.1.3; Scale/2.00)",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


def drawlottery():
    sessionid, userid = readfile();
    url = "http://soagw.pw.szcsckj.com/xllive.pwthunderlottery.s/v1/DrawLottery.json"
    payload = "{'drawLotteryCount':'1','actId':18,'client_plat':2}"
    headers = {
        'Host': "soagw.pw.szcsckj.com",
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Connection': "keep-alive",
        'Cookie': "guid=a26c43c4ca0be8816332d4dedb511698; deviceid=a26c43c4ca0be8816332d4dedb511698; userid=" + userid + "; sessionid=" + sessionid + "; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; appid=1027; sign=3533f21e05a454164bdbecb29bbf52ea; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.3; Scale/2.00)",
        'Accept-Language': "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    return response


def getgiftcontributelist(userid, giftid):
    sessionid, senduserid = readfile();
    url = 'http://soagw.pw.szcsckj.com/xllive.pwgiftwall.s/v1/GetGiftContributeList.json'

    payload = "{'user_id': '" + userid + "', 'gift_id': " + giftid + ",'page':1,'limit':20}"

    headers = {
        'Host': "soagw.pw.szcsckj.com",
        'Accept': "*/*",
        'Cookie': "guid=a26c43c4ca0be8816332d4dedb511698; deviceid=a26c43c4ca0be8816332d4dedb511698; userid=" + senduserid + "; sessionid=" + sessionid + "; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; time=20191213130042; appid=1027; sign=3533f21e05a454164bdbecb29bbf52ea; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.1.3; Scale/2.00)",
        'Accept-Language': "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "text/plain",
        'Cache-Control': "no-cache",
    }

    response = requests.request('POST', url, headers=headers, data=payload)

    print(response.content.decode("utf-8"))


def dealinroom(roomid):
    print('deal in room ' + str(datetime.datetime.now()))
    sessionid, userid = readfile()
    url = "http://soagw.pw.szcsckj.com/xllive.service.online/v1/DealInRoom"
    payload = "{'bizno':'1001','roomid':'" + roomid + "'}"
    headers = {
        'Host': "soagw.pw.szcsckj.com",
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cookie': "guid=a26c43c4ca0be8816332d4dedb511698; deviceid=a26c43c4ca0be8816332d4dedb511698; userid=" + userid + "; sessionid=" + sessionid + "; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; appid=1027; sign=3533f21e05a454164bdbecb29bbf52ea; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.1.3; Scale/2.00)",
        'Accept-Language': "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    checksession(response, roomid)


def checksession(response, roomid):
    if ("ResultCode_NOTLOGIN" in response.text) or ("err session check" in response.text) or (
            "check session failed" in response.text):
        print('session expired')
        readfile(flag=False)
        dealinroom(roomid)
        return True
    else:
        return False


def sendgift(sessionid, roomid, senduserid, acceptuserid):
    print('send gift ' + str(datetime.datetime.now()))
    url = "http://soagw.pw.szcsckj.com/xllive.gift.s/v1/PwSendGift.json"
    payload = "{'roomId':'" + roomid + "','giftId':'1097','sendScene':'1','sendUserid':'" + senduserid + "','isSendAll':'0','sendNum':'1','acceptUserids':['" + acceptuserid + "']} "
    headers = {
        'Host': "soagw.pw.szcsckj.com",
        'Accept': "*/*",
        'Cookie': "guid=a26c43c4ca0be8816332d4dedb511698; deviceid=a26c43c4ca0be8816332d4dedb511698; userid=" + senduserid + "; sessionid=" + sessionid + "; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; time=20191213130042; appid=1027; sign=3533f21e05a454164bdbecb29bbf52ea; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.1.3; Scale/2.00)",
        'Accept-Language': "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "text/plain",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    return response


def keeplive(sessionid, roomid, userid):
    print('keep live ' + str(datetime.datetime.now()))
    url = "http://soagw.pw.szcsckj.com/xllive.service.online/v1/DealPing"
    payload = "{'bizno':'1001','roomid':'" + roomid + "'}"
    headers = {
        'Host': "soagw.pw.szcsckj.com",
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Connection': "keep-alive",
        'Cookie': "guid=a26c43c4ca0be8816332d4dedb511698; deviceid=a26c43c4ca0be8816332d4dedb511698; userid=" + userid + "; sessionid=" + sessionid + "; os=ios; osver=13.1.3; model=iPhone11,8; appver=1.0.0; appcode=3; appid=1027; sign=3533f21e05a454164bdbecb29bbf52ea; channel=inhouse; pushToken=; account_appid=22014",
        'User-Agent': "AudioClub/1.0.0 (iPhone; iOS 13.3; Scale/2.00)",
        'Accept-Language': "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    return response


def login():
    url = "https://xluser-ssl.szcsckj.com/xluser.core.login/v3/login"

    payload = '''
    {
      "appid" : "22014",
      "verifyCode" : "",
      "isCompressed" : "0",
      "verifyKey" : "",
      "deviceName" : "Fucking Awesome",
      "creditkey" : "ck0.XBc1rtXFb5uqIrF1UvKK19fRuYi5XV7mjelIwzH1DXICQZ6MjHMiCJVmBZuE0Jizwh0XvE7tJC0zpctmBI0CouJN7bSZmbjs_v9aQQH8OGnwhuM_JfGa2sJSEE4C_Gc6",
      "devicesign" : "div101.a26c43c4ca0be8816332d4dedb5116984113d07c4047f599c1fcd24ad2509c3c",
      "providerName" : "CTC",
      "sequenceNo" : "1",
      "protocolVersion" : "301",
      "clientVersion" : "3",
      "appName" : "IOS-com.szcsckj.youliao",
      "sdkVersion" : "4.8.2.4",
      "peerID" : "peerid",
      "deviceModel" : "iPhone11,8",
      "passWord" : "''' + os.getenv("PASSWORD") + '''",
      "OSVersion" : "iOS13.1.3",
      "userName" : "''' + os.getenv("USERNAME") + '''",
      "netWorkType" : "WIFI",
      "platformVersion" : "11"
    }'''

    headers = {
        'Host': "xluser-ssl.szcsckj.com",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'User-Agent': "AudioClub/3 CFNetwork/1107.1 Darwin/19.0.0",
        'Accept-Language': "zh-cn",
        'Accept-Encoding': "gzip, deflate, br",
        'Cache-Control': "no-cache",
    }

    response = requests.request('POST', url, data=payload, headers=headers)

    if response.status_code == 200:
        print(response.text)
        sessionpat = '"sessionID":"(\w+\W\w+)'
        session = re.findall(sessionpat, response.text)
        useridpat = '"userID":"(\w+)'
        userid = re.findall(useridpat, response.text)
        return session[0], userid[0]
    else:
        raise Exception


def getluckyinfo():
    url = "http://soagw.pw.szcsckj.com/xllive.pwthunderlottery.s/v1/GetLuckyInfo.json"

    payload = "{'actId':18}"

    response = requests.request("POST", url, data=payload)

    return response


def readfile(flag=True):
    f = open('../cache.txt', 'r+')
    sessionid = f.readline().strip('\n')
    userid = f.readline().strip('\n')
    f.close()
    if sessionid == '' or userid == '' or not flag:
        sessionid, userid = login()
        f = open('../cache.txt', 'w+')
        f.write(sessionid)
        f.write('\n')
        f.write(userid)
        f.close()

    return sessionid, userid


def automaticsendgift(targetroom, targetuser):
    while True:
        sessionid, userid = readfile()
        response = sendgift(sessionid, targetroom, userid, targetuser)

        if checksession(response, targetroom):
            pass
        else:
            break


def autokeeplive(targetroom):
    while True:
        session, userid = readfile()
        response = keeplive(session, targetroom, userid)
        if checksession(response, targetroom):
            pass
        else:
            break


class Logger(object):
    def __init__(self, filename, level=logging.INFO, when='D', backupcount=30,
                 fmt='%(asctime)s - %(filename)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level)
        formatter = logging.Formatter(fmt)
        formatter.default_msec_format = '%s.%03d'
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupcount,
                                               encoding='utf-8')
        th.setFormatter(formatter)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


if __name__ == '__main__':
    getgiftcontributelist('775791522', '1097')
