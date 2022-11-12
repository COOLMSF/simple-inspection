import time

ten_timeArray = time.localtime(time.time())
ten_otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", ten_timeArray)
print(ten_otherStyleTime)

