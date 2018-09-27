# 自定义读取表操作的库
import pandas

# 读取csv文件
def read_file(path):
    return pd.read_csv(path, header=0, encoding='gbk')
