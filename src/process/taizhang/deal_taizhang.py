# _*_ coding=utf-8
# 台账相关处理函数
import pandas as pd
import math
import re
import json

# TableD = ''
zhibiao_path = './relation_file/zhibiao.json'
zhibiao = ''
# 读取csv文件
def read_file(path):
    return pd.read_csv(path, header=0, encoding='gbk')

# 将A表中的数据按户进行划分
def spliteFamily(TableA,TableD):

    # 按照sid区分每一户
    # 先取sid，去掉重复值
    sid_array = TableA["SID"].drop_duplicates()
    # print(sid_array)
    i = 0
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = TableA[TableA["SID"] == sid_index]
        zy_data = TableD[TableD["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='A100')
        # 将表的数据转置显示，显示效果比较接近数据
        # hu_data = hu_data.T
        # print(hu_data)
        if i==5:
            break
        i += 1
        print("============####============")
        print("户：",i)
        print("SID：",hu_data["SID"].values[0])
        taizhang(hu_data,zy_data)
    # print(TableA["SID"])
    # for row in TableA.iterrows():
    #     print(row[1])

# 查找指标代码是否存在与指标代码表中，若不存在，则返回其存在与表中的父类
def findCate(index_code):
    if index_code in zhibiao:
        return index_code
    else:
        while index_code not in zhibiao:
            # print("now zhibiao_code:", index_code)
            index_code = str(int(int(index_code) / 10))
            # if  or index_code == '0':
            #     break
    return index_code

# 判断编码是否有更上层的类别
def hasParent(index_code):
    # 当指标代码不存在与指标表中时，则说明其有所属父类
    while index_code not in zhibiao:
        index_code = str(int(int(index_code) / 10))


# 处理每户的账页数据
def deal_wage_income(hu,zy,wage_code):
    # 将账页表中的所有工资性收入数据取出进行处理
    for wage_index in wage_code:
        wage_income = zy[zy["CODE"] == wage_index]
        # 删除重复人码
        person_code = wage_income["PERSON"].drop_duplicates()
        # print("工资性收入：")
        # print("code:" ,wage_index)
        # 将工资性收入按个人区分开来
        for person_index in person_code:
            # 人码编号99为不区分对应人
            if(int(person_index) < 99):
                # 取对应人码取所有条数的数据
                person_income = wage_income[wage_income["PERSON"] == person_index]
                # 将该人码的金额列相加即为对应编码总的工资性收入
                person_wage = sum(person_income["MONEY"].apply(float))
                # print("A100:")
                # print(type(hu.iloc[0,6]))
                # print("person_index:",person_index,type(person_index))
                person_name = hu[hu["A100"] == int(person_index)]["A101"].values[0]

                wage_index = findCate(wage_index)
                print("类别编码：",wage_index,zhibiao[wage_index],"[第",person_index,"人_",person_name, "]:",person_wage)
            else:
                sum_income = sum(wage_income["MONEY"].apply(float))
                wage_index = findCate(wage_index)
                print("类别编码：",wage_index,zhibiao[wage_index],"总金额：",sum_income)


# 处理每户的工资性收入
def before_deal_wage_income(hu,zy,wage_code):
    # # 编码开头两位是21的表示是工资性收入
    # wage_code = [x for x in zy['CODE'] if re.match(r'^21(.*)', x)]
    # # 去除表中重复的编码
    # wage_code = set(wage_code)
    # print(wage_code)
    # 将账页表中的所有工资性收入数据取出进行处理
    for wage_index in wage_code:
        wage_income = zy[zy["CODE"] == wage_index]
        # 删除重复人码
        person_code = wage_income["PERSON"].drop_duplicates()
        # print("工资性收入：")
        # print("code:" ,wage_index)
        # 将工资性收入按个人区分开来
        for person_index in person_code:
            # 人码编号99为不区分对应人
            if(int(person_index) < 99):
                # 取对应人码取所有条数的数据
                person_income = wage_income[wage_income["PERSON"] == person_index]
                # 将该人码的金额列相加即为对应编码总的工资性收入
                person_wage = sum(person_income["MONEY"].apply(float))
                # print("A100:")
                # print(type(hu.iloc[0,6]))
                # print("person_index:",person_index,type(person_index))
                person_name = hu[hu["A100"] == int(person_index)]["A101"].values[0]
                print("类别编码：",wage_index,"[第",person_index,"人_",person_name, "]:",person_wage)
            else:
                sum_income = sum(wage_income["MONEY"].apply(float))
                print("类别编码：",wage_index,"总金额：",sum_income)

# 处理经营性收入数据
def deal_business_income(hu,zy):
    business_code = [x for x in zy['CODE'] if re.match(r'^22(.*)', x)]
    business_code = set(business_code)
    print(business_code)

    for business_index in business_code:
        business_income = zy[zy["CODE"] == business_index]

# 生成单户台账
# 功能：根据每一户的信息，提取他们对应的台账信息
# 输入：户的A表信息，账页数据表
# 输出：每一户的台账信息
def taizhang(hu,zy):
    global zhibiao
    # print(hu)

    year_arr = zy["YEAR"].drop_duplicates()
    month_arr = zy["MONTH"].drop_duplicates()
    for year_index in year_arr:
        splite_by_year = zy[zy["YEAR"] == year_index]
        for month_index in month_arr:
            splite_by_monyh = zy[zy["MONTH"] == month_index]
            print(year_index, "年", month_index, "月:")
            # 处理工资性收入
            # 编码开头两位是21的表示是工资性收入
            wage_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^21(.*)', x)]
            # 去除表中重复的编码
            wage_code = set(wage_code)
            print("工资性收入：")
            deal_wage_income(hu,splite_by_monyh,wage_code)

            # 编码开头两位是22的表示是经营性收入
            business_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^22(.*)', x)]
            business_code = set(business_code)
            print("经营性收入：")
            deal_wage_income(hu,splite_by_monyh,business_code)

            # 编码开头两位是23的表示是财产性收入
            property_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^23(.*)', x)]
            property_code = set(property_code)
            print("财产性收入：")
            deal_wage_income(hu, splite_by_monyh, property_code)

            # 编码开头两位是24的表示是转移性收入
            transfer_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^24(.*)', x)]
            transfer_code = set(transfer_code)
            print("转移性收入：")
            deal_wage_income(hu, splite_by_monyh, transfer_code)

            # 编码开头两位是25的表示是非收入所得
            not_income_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^25(.*)', x)]
            not_income_code = set(not_income_code)
            print("非收入所得：")
            deal_wage_income(hu, splite_by_monyh, not_income_code)

            # 编码开头两位是26的表示是借贷性所得
            loan_income_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^26(.*)', x)]
            loan_income_code = set(loan_income_code)
            print("借贷性所得：")
            deal_wage_income(hu, splite_by_monyh, loan_income_code)

            # 编码开头两位是53的表示是转移性支出
            transfer_pay_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^53(.*)', x)]
            transfer_pay_code = set(transfer_pay_code)
            print("转移性支出：")
            deal_wage_income(hu, splite_by_monyh, transfer_pay_code)

            # 编码开头两位是13的表示是农林牧渔生产经营成本
            transfer_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^13(.*)', x)]
            transfer_code = set(transfer_code)
            print("农林牧渔生产经营成本：")
            deal_wage_income(hu, splite_by_monyh, transfer_code)

            # 编码开头两位是16的表示是自产自用实物消费
            transfer_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^16(.*)', x)]
            transfer_code = set(transfer_code)
            print("自产自用实物消费：")
            deal_wage_income(hu, splite_by_monyh, transfer_code)

            # 编码开头两位是12的表示是农林牧渔生产经营收入
            transfer_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^12(.*)', x)]
            transfer_code = set(transfer_code)
            print("农林牧渔生产经营收入：")
            deal_wage_income(hu, splite_by_monyh, transfer_code)

            # 编码开头两位是3的表示是生活消费支出
            transfer_code = [x for x in splite_by_monyh['CODE'] if re.match(r'^3(.*)', x)]
            transfer_code = set(transfer_code)
            print("生活消费支出：")
            deal_wage_income(hu, splite_by_monyh, transfer_code)

if __name__ == '__main__':
    A_path = "D:/Document/Code/Python/AuditingApp/src/输入文件夹/A310151.18.csv"
    D_path = "D:/Document/Code/Python/AuditingApp/src/输入文件夹/D310151.1806.csv"
    # zhibiao_path = "D:/Document/Code/Python/AuditingApp/src/输入文件夹/zhibiao_code.csv"
    TableA = read_file(A_path)
    TableD = read_file(D_path)
    with open(zhibiao_path,'r') as f:
        zhibiao = json.load(f)
    spliteFamily(TableA,TableD)


