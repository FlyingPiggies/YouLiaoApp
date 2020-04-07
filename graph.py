import re
import matplotlib.pyplot as plt
from datetime import datetime

times = []
processes = []

with open('logs/GetLuckyInfo.log') as f:
    lines = f.readlines()
    for l in lines:
        tpat = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        time = re.findall(tpat, l)
        ppat = '"process":\"(\d+)'
        process = re.findall(ppat, l)
        date = datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')

        times.append(date.timestamp())
        processes.append(process[0])

fig = plt.figure(figsize=(25,4))
plt.plot(processes, times)
plt.savefig('process.svg')
plt.show()

