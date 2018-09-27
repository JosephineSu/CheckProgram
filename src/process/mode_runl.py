import pandas as pd
import math
import re
import json
from hu import deal_hu
from check import A_necessity_check, A_suggestion_check, B_necessity_check, B_suggestion_check
# TableD = ''
zhibiao_path = './zhibiao.json'
zhibiao = ''
# 读取csv文件
def read_file(path):
    return pd.read_csv(path, header=0)

if __name__ == '__main__':

    #对A表住户成员信息和劳动力从业情况进行审核
    # A_path = u"D:/研一/审核程序/src/输入文件夹/A310151.18.csv"
    # # D_path = "D:/研一/审核程序/src/输入文件夹/D310151.1806.csv", encoding='gbk'
    # # zhibiao_path = "D:/Document/Code/Python/AuditingApp/src/输入文件夹/zhibiao_code.csv"
    # fp = open(A_path)
    # TableA = read_file(fp)
    # # TableD = read_file(D_path)
    # # with open('./zhibiao.json','r') as f:
    # #     zhibiao = json.load(f)
    # hu_data = deal_hu.spliteFamily(TableA)
    # # print()
    # #审核必要性条件
    # for hu in hu_data:
    #     # print(hu)
    #     A_necessity_check.A_necessity_check(hu)
    #
    # pd.set_option('display.width', None)#显示所有数据
    # # 审核提示性条件
    # for hu in hu_data:
    #     print(hu)
    #     A_suggestion_check.A_suggestion_check(hu)

    #对B表住房拥有情况和耐用消费品拥有情况进行审核
    B_path = "D:\研一\审核程序\src\输入文件夹\B310151.18.csv"
    fp2 = open(B_path)
    tableB = read_file(fp2)
    print(tableB.index)
    for row in tableB.iterrows():
        # B_necessity_check.B_necessity_check(row[1])
        B_suggestion_check.B_suggestion_check(row[1])

