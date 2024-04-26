import schedule
import time as tm
from datetime import time, timedelta, datetime

# 實際任務處理部分
def job():
  print("Hello World")


schedule.every().day.at("18:57").do(job)

while True:
  schedule.run_pending()
  tm.sleep(1)
  

# schedule.every(5).seconds.do(job)


# while True:
#   schedule.run_pending()
#   tm.sleep(10)