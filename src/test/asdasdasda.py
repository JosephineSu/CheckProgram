import pandas as pd

fileName1 = 'D:/Document/Code/Python/AuditingApp/data/住户调查科数据及程序/2018年上海住户调查独立审核程序_月（季）报20180427/输入文件夹/A310151.18.csv'
df = pd.read_csv(fileName1,header=0,sep=',',encoding='gbk',error_bad_lines=False)
print('0')
print(df.head())
print("列数",df.columns.size)
print("行数",df.iloc[:,0].size)
print("shuzhi:",df.iat[0,0])
header = df.columns.values.tolist()

print(header)
print(len(header))