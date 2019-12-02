#!/usr/bin/env python3

import sys
import schedule
import time

sys.path.append("../..")
print(sys.path)

from intelligence.task.stockanalysis import mainjob


def test():
    print("test job...")


schedule.every().day.at("14:30").do(mainjob)
while True:
    schedule.run_pending()
    time.sleep(10)