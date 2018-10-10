#A问卷外部审核

import pandas as pd

def read_file(path):
    return pd.read_csv(path, header=0, encoding='gbk')

def ADTableRelationCheck(hu_data):

