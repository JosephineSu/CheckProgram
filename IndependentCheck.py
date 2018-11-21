import pandas as pd
import re
from decimal import Decimal
import datetime

def spliteFamily(table):
    sid_array = table["SID"].drop_duplicates()
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = table[table["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='CODE')
        yield hu_data

def fill4(x):
    return x.zfill(4)

def add_column(zy,codes):
    #在账页表中添加列Sidr,Sidrm,Note4，NNote11，Note22，Note33,Note44
    zy.insert(12,'Sidr',zy['SID']+'p'+zy['PERSON'])
    zy.insert(13,'Sidrm',zy['SID']+'p'+zy['PERSON']+zy['MONTH'])
    pd.set_option('display.width', None)  # 显示所有数据
    # print(zy)
    #为账页中出现的编码添加录入控制码信息
    codes = codes.drop(0)
    # zy = zy.drop(0)
    # print(codes['CODE'])
    x = codes[['CODE', 'note4', 'markyc']]
    df = pd.merge(zy, x, how='left', on=['CODE'])
    df["note4"] = df["note4"].apply(fill4)
    print(type(df['note4']))
    zy.insert(14,'note4',df['note4'])
    zy.insert(15,'note11',df['note4'].apply(lambda x: x[0]))
    zy.insert(16,'note22',df['note4'].apply(lambda x: x[1]))
    zy.insert(17, 'note33', df['note4'].apply(lambda x: x[2]))
    zy.insert(18, 'note44', df['note4'].apply(lambda x: x[3]))
    # zy["note11"] = zy["note11"].apply(lambda x: x[0])
    # zy["note22"] = zy["note22"].apply(lambda x: x[1])
    # zy["note33"] = zy["note33"].apply(lambda x: x[2])
    # zy["note44"] = zy["note44"].apply(lambda x: x[3])

    zy.insert(19,'markyc',df['markyc'])
    # print(zy)
    return zy

def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0

def code_match(table,code):
    pattern = code + "(.*)"
    flag = 0
    for x in table['CODE']:
        if re.match(pattern,x):
            flag = 1
            break
    return flag

# 累计相同类型的账页
def num_same_zy(zy,code):
    pattern = code + "(.*)"
    num = 0
    code = [x for x in zy['CODE'] if re.match(pattern, x)]
    num = len(code)
    return num

def moneySum(zy,code):
    pattern = code + "(.*)"
    code = [x for x in zy['CODE'] if re.match(pattern, x)]
    if len(code) != 0:
        code = set(code)
        code = list(code)
        code.sort()
        frames = []
        for index in code:
            df = zy[zy['CODE'] == index]
            frames.append(df)
        if len(frames) != 0:
            result = pd.concat(frames)
            return sum(result['MONEY'].apply(Decimal))
    return Decimal(0)


#家庭人口
def sum_people(family):
    return len(family.index)


def IndependentCheck(tableA,tableB,zy,zhuhu,zhuzhai,codes):
    zy = zy.drop(0)
    zy = zy.sort_values(by='SID')
    zy = add_column(zy,codes)
    # print(zy)
    zy_families = spliteFamily(zy)
    for zy_family in zy_families:
        family_sid = zy_family['SID'].values[0]
        A = tableA[tableA['SID'] == family_sid]
        B = tableB[tableB['SID'] == family_sid]
        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        print(family_sid)
        if Table(one_zhuhu,'M211') != 1:
            if moneySum(zy_family,"12") > 0:
                print("此户M211不是农业经营户，却出现出售农产品及提供服务编码（12打头），请核实！")

        if Table(one_zhuhu, "M216") == 2:
            if sum_people(A) > 0:
                if moneySum(zy_family, "3") / sum_people(A) < 300:
                    print("此户不是低保户，但月均消费支出不满300元？请核实！")

        #zycheck about tableA and zy
        # if Table(one_zhuhu,'M217') == 1:
        for rowA in A.iterrows():
            A_member = rowA[1]
            person = A_member['A100']
            person_zy = zy_family[zy_family['PERSON'] == str(person)]
            # print(person)

            if A_member['A205'] == 1 and A_member['A204'] == 1 and A_member['A208'] != 0:
                if moneySum(person_zy, "12") + moneySum(person_zy, "2101") + moneySum(person_zy, "22") == 0:
                    print("雇主漏填收入，请核实！")

            if 2 <= A_member['A205'] <= 5 and A_member['A208'] > 0:
                if moneySum(person_zy, "2101") + moneySum(person_zy, "21221") + moneySum(person_zy, "22") == 0:
                    print("此人漏填工资性收入，请核实！")

            if A_member['A204'] != 1 or (A_member['A205'] < 2 or A_member['A205'] > 5) or A_member['A208'] == 0:
                if moneySum(person_zy,"2101") != 0:
                    print("多填工资性收入，请核实！")

            if A_member['A204'] == 1 and A_member['A205'] == 7 and A_member['A208'] != 0:
                if moneySum(person_zy, "22") == 0:
                    print("漏填非农自营收入，请核实！")

            if A_member['A204'] != 1 or A_member['A205'] != 7 or A_member['A208'] == 0:
                if moneySum(person_zy, "22") != 0:
                    print("多填非农自营收入，请核实！")

            if A_member['A206'] != 12:
                if code_match(person_zy, "220911") == 1:
                    print("确有租赁和商务服务收入？请核实并注明具体收入内容！")

            if A_member['A201'] == 1 or A_member['A201'] == 2:
                if A_member['A202'] == 2 and code_match(person_zy, "2401") == 1 and code_match(person_zy,"240111") != 1:
                    print("参加城镇职工养老保险，记账代码应填240111，请核实A202或编码是否正确。")
                if A_member['A202'] == 2 and code_match(person_zy, "2401") == 1 and code_match(person_zy,"240121") != 1:
                    print("参加城镇居民养老保险，记账代码应填240121，请核实A202或编码是否正确。")
                if A_member['A202'] == 4 or A_member['A202'] == 5 and code_match(person_zy, "2401") == 1 and code_match(person_zy, "240191") != 1:
                    print("参加其他养老保险，记账代码应填240191，请核实A202或编码是否正确。")

            if code_match(person_zy, "240111") == 1:
                if A_member['A201'] == 3 and A_member['A202'] != 3 and A_member['A202'] != 4 and A_member['A202'] != 5:
                    print("A201=3，为何有A202（4、5）之外的养老金收入？请核实!")

            if A_member['A106'] >= 60 and A_member['A202'] != 6 and A_member['A202'] != 0 and A_member['A204'] == 2:
                if moneySum(person_zy, "2401") == 0:
                    print("60岁以上为工作参保人员，没有任何养老金收入？请核实！")

            if (A_member['A201'] == 1 or A_member['A201'] == 2) and A_member['A202'] != 4 and A_member['A202'] != 5:
                if code_match(person_zy,"240191") == 1:
                    print("A202≠4,5，为何有其他养老保险收入，请核实！")
                    # print("此人为退休者、A202里面没有4或5，为何有其他养老保险收入，请核实！")

            if A_member['A204'] != 2 and code_match(person_zy, "240811") == 1:
                print("非失业人员，有失业保险金？请核实！")

            if A_member['A201'] == 3 and A_member['A204'] == 1 and A_member['A202'] == 2:
                if moneySum(person_zy, "532111") == 0:
                    print("漏填个人缴纳的养老保险金，请核实！")

            if A_member['A202'] != 1 and A_member['A202'] != 5:
                if code_match(person_zy, "532911") == 1:
                    print("非农保镇保人员，为何有其他社保支出？请注明具体支出内容！")

            if A_member['A205'] != 7:
                if code_match(person_zy, "5513") == 1 or code_match(person_zy, "5514") == 1:
                    print("不是非农自营对象，为何有生产性固定资产支出？请核实并注明具体情况！")

            if A_member['A205'] != 7:
                if code_match(person_zy, "5513") == 1 or code_match(person_zy, "5514") == 1:
                    print("不是非农自营对象，为何有生产性固定资产支出？请核实并注明具体情况！")

            if Table(one_zhuhu, "M216") == 2:
                if sum_people(A) > 0:
                    if moneySum(zy_family, "3") / sum_people(A) < 300:
                        print("此户不是低保户，但月均消费支出不满300元？请核实！")

            # 多填农业自营收入（12 - --15）

            if A_member['A202'] == 4 or A_member['A202'] == 6:
                if code_match(person_zy, "532111") == 1:
                    print("A202=4、6，为何有个人缴纳的养老保险支出，请查改！")

            if A_member['A111'] == 4 or A_member['A111'] == 5 or A_member['A111'] == 7:
                if code_match(person_zy,"532211") == 1:
                    print("A111=4、5、7，为何有个人缴纳的医疗保险支出，请查改")

            if A_member['A111'] == 7 and code_match(person_zy,"240511") == 1:
                print("此人A111=7,为何有报销医疗费用收入,请查改！")

            if A_member['A205'] == 2 or A_member['A205'] == 3 or A_member['A205'] == 4:
                if code_match(person_zy, "210111") == 1 and moneySum(person_zy, "210111") < 2300:
                    print("A205为公职、事业、国企员工，按月发放的工资低于2300元，请核实！")

            if 1 <= A_member['A108'] <= 7 or A_member['A109'] != 1:
                if code_match(person_zy, "533111") == 1:
                    print("A卷该人身份（a108、a109）与记账代码533111不符，请核实！")

            if 1 <= A_member['A108'] <= 7 or A_member['A109'] != 2 and code_match(person_zy, "533211") == 1:
                print("A卷该人身份（a108、a109）与记账代码533211不符。请核实！")

            if A_member['A205'] != 1 and A_member['A100'] == "77":
                print("月度记账人代码77，发生非农经营收入的人应为雇主（a205=1）")

            if A_member['A204'] == 2 or pd.isnull(A_member['A204']) == False:
                if code_match(person_zy, "531111") == 1 or code_match(person_zy, "532311") == 1 or code_match(
                        person_zy, "532411") == 1 or code_match(person_zy, "532911") == 1:
                    print("本季度未从业过（A204），为何发生个税和社会保障支出？请核实并注明原因")

            if A_member['A202'] != 3:
                if code_match(person_zy, "240121") == 1:
                    print("该人为城乡居保收入（240121），为何A202不等于3？请核实并注明原因！")

            if code_match(person_zy, "210291") == 1:
                print("确有其他劳动所得？请核实并注明具体情况")

            if code_match(person_zy, "230911") == 1:
                print("确有其他财产性收入？请注明具体收入内容")

            if code_match(person_zy, "240891") == 1:
                print("确有其他转移性收入？请注明具体收入内容")

            if moneySum(person_zy, "539111") > 500 or moneySum(person_zy, "539211") > 500 or moneySum(person_zy,"539911") > 500:
                print("确有较大金额的其他经常转移支出？(539***)请核实并注明具体支出内容")

            if code_match(person_zy, "522111") == 1:
                print("确有其他财产性支出？请注明具体支出内容")

            for row in person_zy.iterrows():
                person_row = row[1]
                c = int(person_row['CODE'])
                money = float(person_row['MONEY'])
                if 561011 >= c >= 111011 and c != 260111 and c != 560111:
                    if c > 399999 or c < 300000:
                        if money > 50000:
                            print("单笔5万元以上的大额数据，请核实并注明情况！")
                        else:
                            if money > 20000:
                                print("消费单笔2万元以上的大额数据，请核实并注明情况！")
                if person_row['note4'] == 0 and c == 0:
                    print("此条账页的编码（code）,不在标准编码库中，漏填？编码错？导入导出错？请核实！")
                if person_row['markyc'] == 2:
                    print("此条账页的编码（code）为异常编码（这些编码上海应不存在），确有？编码错？导入导出错？请核实！")
                if c != 641111 and c != 651111:
                    if person_row['note11'] == 1 and person_row['AMOUNT'] == 0:
                        print("此条账页应有数据，却漏填数据。请核实！")
                    if person_row['note22'] == 1 and person_row['MONEY'] == 0:
                        print("此条账页应填金额，却漏填金额。请核实！")
                if person_row['note11'] == 0 and person_row['AMOUNT'] != 0:
                    print("此条账页不应填数据，却填了数据。请核实！")
                if person_row['note22'] == 0 and person_row['MONEY'] != 0:
                    print("此条账页不应填金额，却填了金额。请核实！")
                if person_row['note33'] == 1 and person_row['note4'] == 1:
                    print("此条账页应填note4，但是漏填note4内容。请核实！")
                if person_row['note33'] == 0 and person_row['note4'] != 1:
                    print("此条账页不应填note4，却填了note4内容。请核实！")
                p = int(person_row['PERSON'])
                if p < 1 or p > 20 and person_row['note44'] == 1:
                    print("此条账页应填人代码却漏填或填错。请核实！")
                # if c != 0 and person_row['note44'] == 0 and p != 99:
                #     t = code_match(person_row, "3") + code_match(person_row, "52") + code_match(person_row, "54") + code_match(person_row,"55") + \
                #         code_match(person_row, "56") + code_match(person_row, "534111") + code_match(person_row, "539") + code_match(person_row, "23") \
                #         + code_match(person_row, "2402") + code_match(person_row, "2403") + code_match(person_row,"2404") + code_match(person_row,"240711") + \
                #         code_match(person_row, "25") + code_match(person_row, "26") + code_match(person_row, "240821") + code_match(person_row, "240831") + \
                #         code_match(person_row, "240841") + code_match(person_row, "240851") + code_match(person_row,"240861") + code_match(index, "240891")
                #     if t > 0:
                #         print("此条账页人代码应为99，却填为其他值。请核实！")

            if moneySum(person_zy, "240611") > 0 and moneySum(person_zy, "21") > 0:
                print("此人既有工资性收入又有寄带回收入。请核实！")

            if code_match(zy_family, "333307") == 1:
                print("使用管道液化石油气？请核实！")

            if moneySum(person_zy, "260111") >= 10000 and moneySum(person_zy, "230111") == 0:
                print("提取储蓄款万元以上，应有利息收入。请核实！")

            if len(zy_family.index) < 30:
                print("记账笔数少于30笔，请核实并写明原因！")

            if code_match(person_zy, "240131") == 1:
                print("城乡养老保险已经合并成城乡居保，为何发生新型农村社会养老保险收入（240131）请核实！")

            if num_same_zy(person_zy, "532111") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                print("同一人单月个人缴纳的社会保险支出（532111)出现多笔相同金额账页数据")

            if num_same_zy(person_zy, "532211") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                print("同一人单月个人缴纳的社会保险支出（532211)出现多笔相同金额账页数据")

            if num_same_zy(person_zy, "532311") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                print("同一人单月个人缴纳的社会保险支出（532311)出现多笔相同金额账页数据")

            if num_same_zy(person_zy, "532411") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                print("同一人单月个人缴纳的社会保险支出（532411)出现多笔相同金额账页数据")

            #qd 月度数据
            # if Table(one_zhuhu,"M217") == 1:
            #     print("该户账页数据没有录入。")

            if moneySum(person_zy, "240211") != 0 and Table(one_zhuhu, 'M216') == 2:
                print("本月发生低保收入，为何该户不是低保户（M216）？，请核实！")

            if Table(one_zhuhu,"M216") == 1:
                if moneySum(zy_family,"240211") == 0:
                    print("该户为低保户（M216），为何没有低保收入（2402111）？请核实并注明原因！")


            # A问卷
            if Table(one_zhuhu,"M217") == 1 and A_member['A201'] != 3 and A_member['A202'] == 6:
                print("单位离退休人员，为何没有参加任何养老保险A202=6，请核实并注明！")

            if A_member['A108'] == 6:
                print("A108=6,户口登记地在省外，应直接填写省代码！")

            if A_member['A108'] == 7:
                print("A108=7,户口登记地为其他？请核实！")

            a1 = A_member['A111']
            a2 = A_member['A202']
            pk1 = a1 == 1 and a2 != 1
            pk2 = a1 == 2 and a2 != 2
            pk3 = a1 == 3 and a2 != 3
            pk4 = a1 != 1 and a2 == 1
            pk5 = a1 != 2 and a2 == 2
            pk6 = a1 != 3 and a2 == 3
            if pk1 or pk2 or pk3 or pk4 or pk5 or pk6:
                print('A111医疗保险种类与A202养老保险不一致，请核实\n')

            if A_member['A106'] >= 16 and A_member['A112'] == 3 and A_member['A203'] == 2:
                if A_member['A111'] == 4:
                    print('A111确实是公费医疗？请核实并注明具体情况\n')

            if len(str(A_member['A108'])) > 1 and A_member['A204'] == 1:
                if A_member['A111'] == 7:
                    print('外来务工人员，未参加任何医疗保险A111=7，请核实并注明具体情况\n')

            if A_member['A202'] == 6:
                print('外来务工人员，未参加任何养老保险A202=6，请核实并注明具体情况\n')

            if A_member['A204'] == 1 and A_member['A205'] == 6 and A_member['A208'] > 0:
                if moneySum(person_zy, "12") == 0:
                    print("此人漏填农业自营收入（编码12打头）。请核实！")

        #zycheck about tableB and zy
        for rowB in B.iterrows():
            B_family = rowB[1]
            person_SID = B_family['SID']
            person_zy = zy_family[zy_family['SID'] == person_SID]
            print(person_SID)

            if B_family['B130'] == 0 and B_family['B133'] == 0:
                if code_match(person_zy,"2305") == 1:
                    print("多填出租房屋收入。请核实！")

            if B_family['B201'] == 0 and B_family['B202'] == 0 and B_family['B203'] == 0:
                # if per_row['CODE'] == "351311" or per_row['CODE'] == "541111":
                if moneySum(zy_family,"351311") + moneySum(zy_family,"541111") > 0:
                    print("B卷中没有家用汽车、摩托车、燃油助力车，为何发生燃料或机动车保险费？请核实！")

            if B_family['B104'] != 2:
                # if per_row['CODE'] == "331211" and per_row['MONEY'] > '0':
                if moneySum(zy_family,"331211") > 0:
                    print("B卷中房屋来源不是租赁私房，为何发生租赁私房房租费用？请核实并注明原因！")

            if B_family['B104'] != 1:
                # if per_row['CODE'] == "331111" and per_row['MONEY'] > '0':
                if moneySum(zy_family,"331111") > 0:
                    print("B卷中房屋来源不是租赁公房，为何发生租赁公房房租费用？请核实并注明原因！")


            if B_family['B208'] == 0 and code_match(person_zy,"362351") == 1:
                print("Ｂ卷中没有接入有线电视网，为何发生有线电视费用？请核实!")

            if B_family['B126'] == 2:
                if moneySum(zy_family,"521111") > 0:
                    print("B卷B126未在还款，为何发生住房贷款利息支出？请核实并注明原因！")
                if moneySum(zy_family,"560611") > 0:
                    print("B卷中B126未在还款，为何发生归还住房贷款支出？请核实并注明原因！")

            if B_family['B126'] == 1:
                if moneySum(zy_family, "521111") == 0:
                    print("Ｂ卷中B126在还款，为何未发生住房贷款利息支出？漏记或人码有误或B126有误？请核实并注明原因")
                if moneySum(zy_family,"560611") == 0:
                    print("Ｂ卷中B126在还款，为何未发生归还住房贷款支出？漏记或人码有误或B126有误？请核实并注明原因")

            if B_family['B116'] == 5:
                if moneySum(zy_family,"333306") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
                        or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
                    print("B卷中B116=5，本月无管道煤气费用支出。请核实！")
            if B_family['B116'] == 6:
                if moneySum(zy_family,"333305") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
                        or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
                    print("B卷中B116=6，本月无管道天然气费用支出。请核实！")
            if B_family['B116'] == 3:
                if moneySum(zy_family,"333308") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
                        or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
                    print("B卷中B116=3，本月无罐装液化石油气费用支出。请核实！")

            if B_family['B201'] != 0 or B_family['B202'] != 0 or B_family['B203'] != 0:
                if code_match(zy_family,"251311") == 1 or code_match(zy_family,"541111") == 1:
                    print("有汽车或摩托车，无燃料及维修费用支出。请核实")

            # if B_family['B201'] == 0 and B_family['B202'] == 0 and B_family['B203'] == 0:
            #     if per_row['CODE'] == "351311" or per_row['CODE'] == "541111":
            #         print("B卷中没有家用汽车、摩托车、燃油助力车，为何发生燃料或机动车保险费？请核实！")

            if B_family['B104'] != 2 and moneySum(zy_family, "333211") == 0:
                print("本月无电费支出。请核实！")
            # if Table(one_zhuhu,"M217") == 1:
            #     print("该户账页数据没有录入。")
            # if B_family['B116'] == 5:
            #     if moneySum(zy_family,"333306") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
            #             or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
            #         print("B卷中B116=5，本月无管道煤气费用支出。请核实！")
            # if B_family['B116'] == 6:
            #     if moneySum(zy_family,"333305") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
            #             or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
            #         print("B卷中B116=6，本月无管道天然气费用支出。请核实！")
            # if B_family['B116'] == 3:
            #     if moneySum(zy_family,"333308") == 0 and Table(zy_family,"MONTH") == 2 or Table(zy_family,"MONTH") == 5\
            #             or Table(zy_family,"MONTH") == 8 or Table(zy_family,"MONTH") == 11:
            #         print("B卷中B116=3，本月无罐装液化石油气费用支出。请核实！")


            # if moneySum(person_zy,"240211") != 0 and Table(one_zhuhu,'M216') == 2:
            #     print("本月发生低保收入，为何该户不是低保户（M216）？，请核实！")

            # for index,per_row in person_zy.iterrows():
                # if B_family['B130'] == 0 and B_family['B133'] == 0:
                #     if per_row['CODE'] == "230511":
                #         print("多填出租房屋收入。请核实！")

                # if per_row['CODE'] == "240211":
                #     if per_row['MONEY'] != 0 and Table(one_zhuhu,'M216') == 2:
                #         print("本月发生低保收入，为何该户不是低保户（M216）？，请核实！")

                # if B_family['B126'] == 2:
                #     if per_row['CODE'] == "560611":
                #         print("B卷中B126未在还款，为何发生归还住房贷款支出？请核实并注明原因！")
                #     if per_row['CODE'] == "521111":
                #         print("B卷B126未在还款，为何发生住房贷款利息支出？请核实并注明原因！")
                # if B_family['B208'] == 0 and per_row['CODE'] == "362351":
                #     print("B卷中没有接入有线电视网，为何发生有线电视网费用？请核实！")
                # if B_family['B217'] == 0 and B_family['B219'] == 0 and per_row['CODE'] == "352231":
                #     print("B卷中手机与电脑均无接入互联网，为何发生上网费用？请核实！")
                # if B_family['B201'] == 0 and B_family['B202'] == 0 and B_family['B203'] == 0:
                #     if per_row['CODE'] == "351311" or per_row['CODE'] == "541111":
                #         print("B卷中没有家用汽车、摩托车、燃油助力车，为何发生燃料或机动车保险费？请核实！")
                # if B_family['B104'] != 2:
                #     if per_row['CODE'] == "331211" and per_row['MONEY'] > '0':
                #         print("B卷中房屋来源不是租赁私房，为何发生租赁私房房租费用？请核实并注明原因！")
                # if B_family['B104'] != 1:
                #     if per_row['CODE'] == "331111" and per_row['MONEY'] > '0':
                #         print("B卷中房屋来源不是租赁公房，为何发生租赁公房房租费用？请核实并注明原因！")

        # zyselfcheck
        if 310101 <= Table(zy_family,"COUN") <= 310110:
            if code_match(zy_family,"1") == 1:
                print("此户为市中心户，却有1打头的能也账页编码，请核实！")

        if code_match(zy_family,"333307") == 1:
            print("此户本月使用过管道液化石油气？请核实！")

        # for r in zy_family.iterrows():
        #     # print(r)
        #     member = r[1]
        #     people = member['PERSON']
        #     zy_people = zy_family[zy_family['PERSON'] == str(people)]
            # if moneySum(zy_people,"539111") > 500 or moneySum(zy_people,"539211") > 500 or moneySum(zy_people,"539911") > 500:
            #     print("确有较大金额（>500）的其他经常性转移支出？（539***）请核实并注明支出内容！")
            # if moneySum(zy_people,"240611") > 0 and moneySum(zy_people,"21") > 0:
            #     print("此人既有工资性收入又有寄带回收入。请核实！")
            # if code_match(zy_people,"532111") + code_match(zy_people,"532211")+code_match(zy_people,"532311")+code_match(zy_people,"532311")\
            #     +code_match(zy_people,"532411")+code_match(zy_people,"532911")> 1:
            #     print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
            # if num_same_zy(zy_people,"532") > 1:
            #     print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
            # for single in zy_people.iterrows():
            #     index = single[1]
            #     c = int(index['CODE'])
            #     money = float(index['MONEY'])
            #     if 561011 >= c >= 111011 and c != 260111 and c != 560111:
            #         if c > 399999 or c < 300000:
            #             if money > 50000:
            #                 print("单笔5万元以上的大额数据，请核实并注明情况！")
            #         else:
            #             if money > 20000:
            #                 print("消费单笔2万元以上的大额数据，请核实并注明情况！")
            #     if c == 210291:
            #         print("确有其他劳动所得？请注明具体支出内容")
            #     if c == 522111:
            #         print("确有其他财产性支出？请注明具体支出内容")
            #     if c == 230911:
            #         print("确有其他财产性收入？请注明具体收入内容")
            #     if c == 240891:
            #         print("确有其他转移性收入？请注明具体收入内容")
            #     if c == 333307:
            #         print("使用管道石油液化气？（非金山、崇明）")
            #     if c == 260111 and money >= 10000 and moneySum(zy_people,"230111") == 0:
            #             print("提取储蓄款万元以上，应有利息收入。请核实！")
            #     if index['note4'] == 0 and c == 0:
            #         print("此条账页的编码（code）,不在标准编码库中，漏填？编码错？导入导出错？请核实！")
            #     if index['markyc'] == 2:
            #         print("此条账页的编码（code）为异常编码（这些编码上海应不存在），确有？编码错？导入导出错？请核实！")
            #     if c != 641111 and c != 651111:
            #         if index['note11'] == 1 and index['AMOUNT'] == 0:
            #             print("此条账页应有数据，却漏填数据。请核实！")
            #         if index['note22'] == 1 and index['MONEY'] == 0:
            #             print("此条账页应填金额，却漏填金额。请核实！")
            #     if index['note11'] == 0 and index['AMOUNT'] != 0:
            #         print("此条账页不应填数据，却填了数据。请核实！")
            #     if index['note22'] == 0 and index['MONEY'] != 0:
            #         print("此条账页不应填金额，却填了金额。请核实！")
            #     if index['note33'] == 1 and index['note4'] == 1:
            #         print("此条账页应填note4，但是漏填note4内容。请核实！")
            #     if index['note33'] == 0 and index['note4'] != 1:
            #         print("此条账页不应填note4，却填了note4内容。请核实！")
            #     p = int(index['PERSON'])
            #     if p < 1 or p > 20 and index['note44'] == 1:
            #         print("此条账页应填人代码却漏填或填错。请核实！")
            #     if c == 240131:
            #         print("城乡养老保险已经合并成城乡居保，为何发生新型农村社会养老保险收入（240131）请核实！")
            #     if c != 0 and index['note44'] == 0 and p != 99:
            #         t = code_match(index,"3") + code_match(index,"52")+ code_match(index,"54")+ code_match(index,"55")+\
            #             code_match(index,"56")+ code_match(index,"534111")+ code_match(index,"539")+ code_match(index,"23") \
            #             + code_match(index, "2402")+ code_match(index,"2403")+code_match(index,"2404")+ code_match(index,"240711")+\
            #             code_match(index,"25")+ code_match(index,"26")+ code_match(index,"240821")+ code_match(index,"240831")+ \
            #             code_match(index, "240841")+ code_match(index,"240851")+ code_match(index,"240861")+ code_match(index,"240891")
            #         if t > 0:
            #             print("此条账页人代码应为99，却填为其他值。请核实！")

# 打开csv文件 返回DataFrame对象
def read_csv(path):
    with open(path, 'r') as f:
        file = pd.read_csv(f, header=0)
    return file

if __name__ == '__main__':
    A_path = u"D:/研一/审核程序/src/输入文件夹/A310151.18.csv"
    B_path = u"D:/研一/审核程序/src/输入文件夹/B310151.18.csv"
    zy_path = u"D:/研一/审核程序/src/输入文件夹/D310151.1806.csv"
    zhuhu_path = u"D:/研一/审核程序/src/输入文件夹/住户样本310151.18.csv"
    zhuzhai_path = u"D:/研一/审核程序/src/输入文件夹/住宅名录310151.18.csv"
    codes_path = "D:\研一\项目\CheckProgram\Auditing\输入文件夹\编码手册.csv"
    # fp2 = open(codes_path)
    codes = read_csv(codes_path)

    TableA = read_csv(A_path)
    TableB = read_csv(B_path)
    zy = read_csv(zy_path)
    zhuzhai = read_csv(zhuzhai_path)
    zhuhu = read_csv(zhuhu_path)

    IndependentCheck(TableA,TableB,zy,zhuhu,zhuzhai,codes)
