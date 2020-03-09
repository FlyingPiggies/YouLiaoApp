from multiprocessing import Process

import schedule

from Util import automaticsendgift, autokeeplive, dealinroom


def sendgift(targetroomid, targetuserid):
    schedule.every(5.05).minutes.do(automaticsendgift, targetroom=targetroomid, targetuser=targetuserid)

    while True:
        schedule.run_pending()


def keeplive(targetroom):
    schedule.every(15).seconds.do(autokeeplive, targetroom=targetroom)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # '2_70208' bj
    # '2_72518' self
    targetroomid = '2_72518'
    targetuserid = '775791522'
    dealinroom(targetroomid)
    p1 = Process(target=sendgift, args=(targetroomid, targetuserid))
    p2 = Process(target=keeplive, args=(targetroomid,))
    p1.start()
    p2.start()
