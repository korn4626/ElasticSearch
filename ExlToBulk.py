from openpyxl import load_workbook
from dateutil.relativedelta import relativedelta
import random
import datetime

# data_only=True로 해줘야 수식이 아닌 값으로 받아온다. 
def load_exl(filepath, header=0, sheet=None):
    ret = {}
    load_wb = load_workbook(filepath, data_only=True)
    # print(load_wb._sheets[0].__dict__)
    if sheet is not None:
        st = load_wb[sheet]
        index = st.title
        all_values = []
        cols = []
        for idx, row in enumerate(st.rows):
            row_value = {}
            if idx < header:
                pass
            elif idx == header:#컬럼명
                for cell in row:
                    if cell.value : 
                        cols.append(cell.value)
            else:
                for i, cell in enumerate(row):
                    if i == 0 and cell.value is None:
                        break
                    if i < len(cols):
                      #자료형 변환
                        if "YMD" in cols[i]:
                            tmp = str(cell.value).replace("-", "")[:8]
                            row_value[cols[i]] = "{0}-{1}-{2}".format(tmp[:4], tmp[4:6], tmp[-2:])
                        elif "CNT" in cols[i]:
                            row_value[cols[i]] = int(str(cell.value))
                        else:
                            row_value[cols[i]] = cell.value
                if row_value:
                    all_values.append(row_value.copy())
        ret[index] = all_values.copy()
    else:
        for st in load_wb._sheets:
            index = st.title
            all_values = []
            cols = []
            row_value = {}
            for idx, row in enumerate(st.rows):
                row_value = {}
                if idx < header:
                    pass
                elif idx == header:#컬럼명
                    for cell in row:
                        if cell.value : 
                            cols.append(cell.value)
                else:
                    for i, cell in enumerate(row):
                        if i == 0 and cell.value is None:
                            break
                        if i < len(cols):
                            if "YMD" in cols[i]:
                                tmp = str(cell.value).replace("-", "")[:8]
                                row_value[cols[i]] = "{0}-{1}-{2}".format(tmp[:4], tmp[4:6], tmp[-2:])
                            elif "CNT" in cols[i]:
                                row_value[cols[i]] = int(str(cell.value))
                            else:
                                row_value[cols[i]] = cell.value
                    if row_value:
                        all_values.append(row_value.copy())
            ret[index] = all_values.copy()
                
    return ret

import json
data = load_exl("xlsFile경로명.xls", 1)

#ElasticSearch Bulk Query만들기.
for key in data:
    for d in data[key]:
        t = '{{"index":{{"_index":"{0}"}}}}\n'.format(key.lower())
        x = ""
        x += json.dumps(d)+"\n"
        with open("bulk.json", "a") as f:
            f.write(t+x)

#Bulk데이터 전송 2가지 방안
# import os
# os.system("curl -XPOST \"http://엘라스틱경로:9200/_bulk\" -H 'Content-Type: application/json' --data-binary @bulk.json")

# import requests
# r = requests.post('http://엘라스틱경로:9200/_bulk', data=open('bulk.json','rb'), headers={'Content-Type': 'application/json'})
