import sys
import schedule
import time

sys.path.append("../..")
print(sys.path)

from intelligence.schedulejob.stockanalysis import mainjob
def test():
    print("test job...")
# while True:
#     print("start...")
    # schedule.every().day.at("23:47").do(test)
    # time.sleep(10)


schedule.every().day.at("23:51").do(mainjob)
while True:
    schedule.run_pending()
    time.sleep(10)