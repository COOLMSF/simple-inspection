import os
import sys

from openpyxl import Workbook

current_path = os.path.dirname(__file__)
sys.path.append(current_path)

import cbh
import dba02


wb = Workbook()

cbh.CBH_CHECK(wb)
dba02.DBA_CHECKOUT(wb)

wb.save('bastion_host_result.xlsx')



