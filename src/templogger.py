from tempsender import Tempsender
import time
from datetime import datetime
import csv
ts = Tempsender()

with open ('debug/temperatures.csv','a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date','alice','bob'])
    while True:
        print('ping')
        ts.poll() 
        at = ts.get_stats("alice", "temperature", "last")
        bt = ts.get_stats("bob", "temperature", "last") 
        date = datetime.now()
        writer.writerow([date, at, bt])
        time.sleep(0.5)



