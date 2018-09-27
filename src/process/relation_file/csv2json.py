import pandas as pd
import json
# 读取csv文件
def read_file(path):
    return pd.read_csv(path, header=0, encoding='gbk')

def csv2json(zb):
    keys = zb["code"].fillna(9999).apply(int) #fillna()填充nan,返回9999
    keys = keys.apply(str)
    values = zb["desc"].apply(str)
    print(len(keys),len(values))
    zhibiao = {}
    for key,value in zip(keys,values):
        print(key,value)
        zhibiao[key] = value
    print("zhibiao:")
    print(zhibiao)
    with open('./zhibiao.json','w+') as f:
        f.write(json.dumps(zhibiao))##dumps将dict转化成str格式
    print('ok')


if __name__ == '__main__':
    zhibiao_path = "D:\研一\审核程序\src\输入文件夹\zhibiao_code.csv"
    zb = read_file(zhibiao_path)
    csv2json(zb)
