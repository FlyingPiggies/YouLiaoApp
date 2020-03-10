import logging
import re
import time

from Util.Util import getluckyinfo, Logger


def autogetluckyinfo():
    process = 0
    while True:
        response = getluckyinfo()
        pat = '"process":\"(\d+)'
        result = re.findall(pat, response.text)
        if process != result[0]:
            log.logger.info(response.text)
            if process != 0:
                # drawlottery()
                pass
            process = result[0] 
        time.sleep(0.5)


log = Logger(filename='Logs/GetLuckyInfo.log',
             level=logging.DEBUG)

autogetluckyinfo()
