import sys
import requests
import json
import xlwt


# add parent directory to import module
# sys.path.append("..")
stocks_to_be_saved_sorted = []
header = ["bond_id", "bond_nm", "stock_id", "price", "premium_rt", "calculated_result"]
properties_dict = {}


def __init__():
    from intelligence.util.Util import Properties
    global properties_dict
    properties_dict = Properties("../config/bond_info_config").getProperties()


def takecomparekey(item):
    sourt_key = item.get("calculated_result")
    # print(sourt_key)
    return float(sourt_key)


def writetoexcel(header, content, savedpath):
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("S1", cell_overwrite_ok=True)
    for i in range(len(header)):
        ws.write(0, i, header[i])

    for row_index in range(len(content)):
        row = content[row_index]
        body = list(row.values())
        print(body)
        print(len(body))
        for i in range(len(body)):
            ws.write(row_index + 1, i, body[i])

    wb.save(savedpath)


def getbondlist():
    response = requests.get("https://www.jisilu.cn/data/cbnew/delisted/")  # 已退市转债列表
    response = requests.get("https://www.jisilu.cn//data/cbnew/cb_list/")
    response.encoding = 'utf-8'

    response_content = response.text
    # bs4_format = BeautifulSoup(response_content, "html.parser")

    response_json = json.loads(response_content)

    stocks_to_be_saved = []

    list_dict = json.loads(response_content).get("rows")
    for item in list_dict:
        stock = {}
        stock['bond_id'] = item.get("cell").get("bond_id")
        stock['bond_nm'] = item.get("cell").get("bond_nm")
        stock['stock_id'] = item.get("cell").get("stock_id")
        stock['price'] = item.get("cell").get("price")
        stock['premium_rt'] = item.get("cell").get("premium_rt")
        premium_rt = float(stock['premium_rt'].replace('%', ''))
        calculated = float(stock['price']) + premium_rt
        stock['calculated_result'] = ("%.3f" % calculated)  # decimal 3 digits
        stocks_to_be_saved.append(stock)
        print(stock)
        print("\n")

    stocks_to_be_saved_sorted = sorted(stocks_to_be_saved, key=takecomparekey)
    return stocks_to_be_saved_sorted


def mainjob():
    __init__()
    stocks_to_be_saved_sorted = getbondlist()
    print("number of stocks to be saved:" + str(len(stocks_to_be_saved_sorted)))

    output_path = properties_dict.get("output_path")
    file_name = properties_dict.get("file_name")
    writetoexcel(header, stocks_to_be_saved_sorted, output_path + file_name)
    print("Successfully generate the excel in " + output_path)

    from intelligence.emailfunc import sendemail
    email_addr = properties_dict.get("email_receiver")
    email_addr_list = email_addr.split(',')
    for email in email_addr_list:
        print("send file to email " + email_addr)
        sendemail.sendExcel(email, "可转债列表", output_path + file_name, file_name)
