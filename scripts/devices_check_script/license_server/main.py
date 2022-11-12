import os
import sys

from openpyxl import Workbook

current_path = os.path.dirname(__file__)
sys.path.append(current_path)

import cbh
import dba
import log


wb = Workbook()

cbh.CBH_CHECK(wb)
dba.DBA_CHECKOUT(wb)
log.LOG_CHECKOUT(wb)


wb.save('巡检资料.xlsx')
print(f'输出的文件在：{os.getcwd()}')



