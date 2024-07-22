import time
import asyncio

def task():
    print("Start of sync task")
    time.sleep(5)
    print("After 5 second of sleep")


start = time.time()
for i in range(3):
    task()
duration = time.time() - start
print("Process completed in  : {}-seconds".format(duration))
