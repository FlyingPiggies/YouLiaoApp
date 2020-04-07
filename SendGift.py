import schedule
from multiprocessing import Process
from Util import sendgift, keeplive, dealinroom, login


def automaticsendgift(sessionid, userid, targetroomid, targetuserid):
    schedule.every(5.05).minutes.do(sendgift, sessionid=sessionid, roomid=targetroomid, senduserid=userid,
                                    acceptuserid=targetuserid)

    while True:
        schedule.run_pending()


def autokeeplive(sessionid, userid, targetroomid):
    schedule.every(15).seconds.do(keeplive, sessionid=sessionid, roomid=targetroomid, userid=userid)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # '2_70208' bj
    # '2_72518' self
    targetroomid = '2_72518'
    targetuserid = '775791522'
    sessionid, userid = login()
    dealinroom(sessionid, userid, targetroomid)
    p1 = Process(target=automaticsendgift, args=(sessionid, userid, targetroomid, targetuserid))
    p2 = Process(target=autokeeplive, args=(sessionid, userid, targetroomid,))
    p1.start()
    p2.start()
