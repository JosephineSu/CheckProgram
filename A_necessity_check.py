# 指标行数:100
# ********************************
# *   全国住户生活状况调查季报   *
# *         问卷A审核公式        *
# *        2015年08月23日        *
# ********************************
import pandas as pd
# import numpy as np
import datetime
from deal_hu import spliteFamily
import myLogging as mylogger


Year = datetime.datetime.now().year
Month = datetime.datetime.now().month

A_necessity_data = {'sid':[],'scode':[],'name':[],'code':[],'提示内容':[],'townname':[],'vname':[]}
A_necessity_result = pd.DataFrame(A_necessity_data)
A_necessity_result = A_necessity_result[['sid','scode','name','code','提示内容','townname','vname']]

def insert_to_pd(data):
    global A_necessity_result
    A_necessity_result = A_necessity_result.append(data, ignore_index=True)

def read_file(path):
    with open(path) as f:
        return pd.read_csv(f, header=0)

# 将A表中的数据按户进行划分
def spliteFamily(TableA):

    # 按照sid区分每一户
    # 先取sid，去掉重复值
    sid_array = TableA['SID'].drop_duplicates()
    # print(sid_array)
    i = 0
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = TableA[TableA['SID'] == sid_index]
        # zy_data = TableD[TableD["SID"] == sid_index]

        hu_data = hu_data.sort_values(by='A103')#按照与本户户主关系排序
        yield hu_data


def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0


def A_necessity_check(TableA,zhuhu,xiaoqu):
    mylogger.logger.debug("A_necessity_check init..")
    result = open(r'..\Auditing\审核结果输出\A_necessity_check_result.txt', 'w')
    hu_total = spliteFamily(TableA)
    for hu in hu_total:
        A,M=9101,993
        psA,psB=0,0
        hzAge,xb,hz,po=0,0,0,0
        # print(hu)
        family_sid = TableA['SID'].values[0]
        one_zhuhu = zhuhu[zhuhu["HHID"] == family_sid]
        scode = TableA['SCODE'].values[0]

        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['vID'] == qu_vid]
        townname = qu['townName'].values[0]
        vname = qu['vName'].values[0]

        dict = {'sid':family_sid,'scode':scode,'townname':townname,'vname':vname}

        for index, A_table in hu.iterrows():
            result.write(A_table['SID']+A_table['A101'] + '\n')
            # if A_table['A102'] == 3:
            #     continue
            # print(A_table['SID'])
            # print(index)
            # print(A_table)
            # while(A < 9120):
            person = A_table['A100']
            name = A_table['A101']
            dict['name'] = name

            if person == 0:
                result.write("请更新家庭成员情况(A1)\n")
                value = "A100={}".format(person)
                dict['code'] = value
                dict['提示内容'] = "请更新家庭成员情况（A1）"
                insert_to_pd(dict)
            else:
                result.write('')

            if person > 0:
                psA += 1
                if pd.isnull(A_table['A200']) == False:
                    if person != A_table['A200']:
                        value = "A200={}".format(A_table['A200'])
                        dict['code'] = value
                        dict['提示内容'] = "问卷A有问题请在问卷录入窗口,请修正!"
                if A_table['A102'] % 4 == 3:
                    A += 1
                    continue
                psB += 1
                if A_table['A103'] == 1:
                    hzAge = A_table['YEAR'] - A_table['A105_1']
                    hz += 1
                    xb = A_table['A104']

                data = A_table['A103']
                if data == 2: po += 1
                if data == 2:
                    if A_table['A104'] == xb:
                        value = "A104={}".format(A_table['A104'])
                        dict['code'] = value
                        dict['提示内容'] = "户主与配偶性别相同"
                        insert_to_pd(dict)

                AAAAAAAA = 1
                if A_table['A105'] is None:
                    dict['code'] = "A105={}".format(A_table['A105'])
                    dict['提示内容'] = "请补填年龄，不足1岁请填写0"
                tbAge = Year - A_table['A105_1'] #填报的年龄
                tbYear = A_table['A105_1']
                tbMonth = A_table['A105_2']
                Age = Year-tbYear
                # 实际年龄
                if Month < tbMonth: Age -= 1

                # A1部分
                # 应该填报内容
                # A102开户时填4，其他时间非4，但每个报告期都可能开户
                # A102 == c4 ?: "人员增减情况越界，请填写(4)"
                # 开户时，应直接填报"4"
                if A_table['A102'] < 1 or A_table['A102'] > 4:
                    result.write("人员增减情况越界，请填写(1-4)\n")
                if A_table['A103'] < 1 or A_table['A103'] > 10:
                    result.write("与本户户主的关系越界，请填写(1-10)\n")
                if A_table['A104'] != 1 and A_table['A104'] != 2:
                    result.write("性别越界，请填写(1-2)\n")
                if tbYear == Year:
                    if tbMonth > Month:
                        result.write("出生月份越界\n")
                if A_table['A105'] < 191001 or A_table['A105'] > Year * 100 + Month:
                    result.write("出生年月越界\n")
                if A_table['A107'] < 1 or A_table['A107'] > 9:
                    result.write("民族越界，请填写(1-9)\n")
                if A_table['A108'] != 1 and A_table['A108'] != 2 and A_table['A108'] != 3 and A_table['A108'] !=  4 and\
                        A_table['A108'] != 5 and A_table['A108'] != 7 and A_table['A108'] != 11 and A_table['A108'] != 12\
                        and A_table['A108'] != 13 and A_table['A108'] != 14 and A_table['A108'] != 15 and A_table['A108'] !=21\
                        and A_table['A108'] != 22 and A_table['A108'] != 23 and A_table['A108'] != 31 and A_table['A108'] != 32\
                        and A_table['A108'] != 33 and A_table['A108'] != 34 and A_table['A108'] != 35 and A_table['A108'] != 36\
                        and A_table['A108'] != 37 and A_table['A108'] != 41 and A_table['A108'] != 42 and A_table['A108'] != 43\
                        and A_table['A108'] != 44 and A_table['A108'] != 45 and A_table['A108'] != 46 and A_table['A108'] != 50\
                        and A_table['A108'] != 51 and A_table['A108'] != 52 and A_table['A108'] != 53 and A_table['A108'] != 54\
                        and A_table['A108'] != 61 and A_table['A108'] != 62 and A_table['A108'] != 63 and A_table['A108'] != 64\
                        and A_table['A108'] != 65 and A_table['A108'] != 71 and A_table['A108'] != 81 and A_table['A108'] != 82:
                    result.write("户口登记地越界，请重新填写\n")

                if A_table['A109'] < 1 or A_table['A109'] > 3: result.write("户口性质越界，请填写(1-3)\n")
                if A_table['A110'] < 1 or A_table['A110'] > 4: result.write("健康状况越界，请填写(1-4)\n")

                if Table(one_zhuhu,'M205') == 4:
                    if A_table['A110'] == 4:
                        result.write("住家保姆、帮工,生活不能自理？")
                    if A_table['A112'] != 3:
                        result.write("住家保姆、帮工,不能是在校学生？")

                if A_table['A111'] is None: result.write("A111漏填，若没有参加医疗保险请填7\n")
                if Age >= 6:
                    if A_table['A112'] < 1 or A_table['A112'] > 3:
                        result.write("是否在校生越界，请填写(1-3)\n")
                    if A_table['A113'] < 1 or A_table['A113'] > 7:
                        result.write("教育程度越界，请填写(1-7)\n")
                if Age >= 15:
                    if A_table['A114'] < 1 or A_table['A114'] > 4:
                        result.write("婚姻状况越界，请填写(1-4)\n")
                if A_table['A115'] is None: result.write("A115漏填，若本季度未在家居住请填0\n")
                if A_table['A115'] > 3: result.write("本季度居住时间越界\n")
                if A_table['A116'] != 1 and A_table['A116'] != 2: result.write("是否其它住宅居住越界，请填写(1-2)\n")
                if A_table['A117'] != 1 and A_table['A117'] != 2: result.write("是否在本住宅居住一天以上越界，请填写(1-2)\n")
                if A_table['A118'] != 1 and A_table['A118'] != 2: result.write("是否打算居住一个半月以上越界，请填写(1-2)\n")
                if A_table['A119'] != 1 and A_table['A119'] != 2: result.write("是否常住人口越界，请填写(1-2)\n")
                if A_table['A120'] != 1 and A_table['A120'] != 2: result.write("是否是否持证残疾人越界，请填写(1-2))\n")

                # 应该跳转内容
                if A_table['A112'] + A_table['A113'] > 0:
                    if Age < 6:
                        result.write("小于6岁，不用填报A112|A113\n")
                if A_table['A114'] > 0:
                    if Age < 15:
                        result.write("小于15岁，不用填报A114\n")
                if Age < 15 or A_table['A112'] != 3:
                    # age < c15 | | A112 != c3? A201 + +A208 > c0 ?"小于15岁或在校生，不用填报A2问卷":: // 可能按虚岁填报
                    if A_table['A201'] + A_table['A208'] > 0:
                        result.write("小于15岁或在校生，不用填报A2问卷\n")
                if A_table['A112'] != 3:
                    if A_table['A113'] == 1:
                        result.write("在校生没上过学？\n")
                    else:
                        if Age > 14 and A_table['A113'] < 3:
                            result.write("14周岁以上在校生，学历低于小学？\n")
                        if Age > 17 and A_table['A113'] < 4:
                            result.write("17周岁以上在校生，学历低于初中？\n")
                        if Age > 20 and A_table['A113'] < 5:
                            result.write("20周岁以上在校生，学历低于高中？\n")
                        if Age > 24 and A_table['A113'] < 6:
                            result.write("24周岁以上在校生，学历低于大学？\n")

                if A_table['A108'] == 'U':
                    result.write("户口在本省，不用填省码\n")

                if A_table['A119'] != 1:
                    if A_table['A115'] >= 1.5 or A_table['A118'] == 1:
                        result.write("满足条件A，应视为常住人口\n")
                    if A_table['A116'] == 2 and A_table['A117'] == 1:
                        result.write("满足条件b，应视为常住人口\n")
                    if A_table['A112'] == 1:
                        result.write("满足条件c,应视为常住人口\n")

                # //***************A2部分*****************
                # //劳动力部分全部都是A，跟第一部分A不一样。
                if Age >= 16 and A_table['A112'] == 3 and A_table['A200'] is None:
                    result.write("16岁及以上非在校生应填写A2部分\n")
                    A += 1
                if Age >= 16 and A_table['A112'] == 3 and pd.isnull(A_table['A200'])==False:
                    #应该填报内容
                    if A_table['A201'] != 1 and A_table['A201'] != 2 and A_table['A201'] != 3:
                        result.write("是否离退休越界，请填写(1-3)\n")
                    if pd.isnull(A_table['A202']) == True:
                        result.write("A202漏填，若没有参加养老保险请填6\n")
                    if A_table['A203'] != 1 and A_table['A203'] != 2:
                        result.write("是否丧失劳动力越界，请填写(1-2)\n")
                    if A_table['A203'] == 2:
                        if A_table['A204'] != 1 and A_table['A204'] != 2:
                            result.write("是否从业过越界，请填写(1-2)\n")
                        if A_table['A204'] == 1:
                            if A_table['A205'] < 1 or A_table['A205'] > 7:
                                result.write("就业类型越界，请填写(1-7)\n")
                            if A_table['A206'] < 1 or A_table['A206'] > 20:
                                result.write("行业越界，请填写(1-20)\n")
                            if A_table['A207'] < 1 or A_table['A207'] > 8:
                                result.write("工作种类越界，请填写(1-8)\n")
                            if A_table['A208'] < 0.1 or A_table['A208'] > 3:
                                result.write("工作总时间越界\n")
                            if A_table['A209'] != 1 and A_table['A209'] != 2 and A_table['A209'] != 3 and A_table['A209'] != 4 and \
                                A_table['A209'] != 5 and A_table['A209'] != 7 and A_table['A209'] != 11 and A_table['A209'] != 12 \
                                and A_table['A209'] != 13 and A_table['A209'] != 14 and A_table['A209'] != 15 and \
                                A_table['A209'] != 21 and A_table['A209'] != 22 and A_table['A209'] != 23 and A_table['A209'] != 31 and \
                                A_table['A209'] != 32 and A_table['A209'] != 33 and A_table['A209'] != 34 and A_table['A209'] != 35 and \
                                A_table['A209'] != 36 and A_table['A209'] != 37 and A_table['A209'] != 41 and A_table['A209'] != 42 and \
                                A_table['A209'] != 43 and A_table['A209'] != 44 and A_table['A209'] != 45 and A_table['A209'] != 46 and \
                                A_table['A209'] != 50 and A_table['A209'] != 51 and A_table['A209'] != 52 and A_table['A209'] != 53 and \
                                A_table['A209'] != 54 and A_table['A209'] != 61 and A_table['A209'] != 62 and A_table['A209'] != 63 and \
                                A_table['A209'] != 64 and A_table['A209'] != 65 and A_table['A209'] != 71 and A_table['A209'] != 81 and \
                                A_table['A209'] != 82 and A_table['A209'] != 83:
                                result.write("本季度工作地点越界，请重新填写\n")
                            if A_table['A210'] != 1 and A_table['A210'] != 2 and A_table['A210'] != 3 and A_table['A210'] != 11\
                                and A_table['A210'] != 12 and A_table['A210'] != 13 and A_table['A210'] != 14 and A_table['A210'] != 15\
                                and A_table['A210'] != 21 and A_table['A210'] != 22 and A_table['A210'] != 23 and A_table['A210'] != 31\
                                and A_table['A210'] != 32 and A_table['A210'] != 33 and A_table['A210'] != 34 and A_table['A210'] != 35\
                                and A_table['A210'] != 36 and A_table['A210'] != 37 and A_table['A210'] != 41 and A_table['A210'] != 42\
                                and A_table['A210'] != 43 and A_table['A210'] != 44 and A_table['A210'] != 45 and A_table['A210'] != 46\
                                and A_table['A210'] != 50 and A_table['A210'] != 51 and A_table['A210'] != 52 and A_table['A210'] != 53\
                                and A_table['A210'] != 54 and A_table['A210'] != 61 and A_table['A210'] != 62 and A_table['A210'] != 63\
                                and A_table['A210'] != 64 and A_table['A210'] != 65 and A_table['A210'] != 71 and A_table['A210'] != 81\
                                and A_table['A210'] != 82 and A_table['A210'] != 83:
                                result.write("最远工作或学习地点越界，请重新填写\n")
                            if A_table['A211'] < 1 or A_table['A211'] > 8:
                                result.write("主要群体种类越界，请填写(1-8)\n")
                            if A_table['A212'] < 1 or A_table['A212'] > 8:
                                result.write("次要群体种类越界，请填写(1-8)\n")
                            if A_table['A213'] < 1 or A_table['A213'] > 4:
                                result.write("最高技能证书越界，请填写(1-4)\n")
                            if A_table['A214'] < 1 or A_table['A214'] > 4:
                                result.write("最高证书职称越界，请填写(1-4)\n")
                            if A_table['A211'] == 8 and A_table['A212'] < 8:
                                result.write("主要群体种类为不属于任何群体，次要群体种类也应不属于任何群体\n")
                            if A_table['A211'] > 0 and A_table['A211'] < 8 and A_table['A211'] == A_table['A212']:
                                result.write("主要群体和次要群体填写内容一致\n")

                    if Table(one_zhuhu,"M205") == 4:
                        if A_table['A203'] != 2:
                            result.write("住家保姆、帮工,或集体居住户,不能丧失劳动能力\n")
                        if A_table['A204'] != 1:
                            result.write("住家保姆、帮工,A204要填从业\n")
                        if A_table['A205'] != 5:
                            result.write("住家保姆、帮工,应该是其他雇员\n")

                    # 应该跳转内容
                    sum = A_table['A205'] + A_table['A206'] +A_table['A207'] +A_table['A208']
                    if A_table['A204'] + sum > 0:
                        if A_table['A203'] == 1:
                            result.write("丧失劳动力，不用填报A204-A208\n")
                    if sum > 0 and A_table['A204'] == 2:
                        result.write("本季未从业，不用填报A205-A208\n")

                    # 逻辑关系
                    if (A_table['A203'] == 2 or A_table['A204'] == 1) and A_table['A110'] == 4:
                        result.write("生活不能自理，还具有劳动能力?\n")
                    if A_table['A204'] == 1 and A_table['A208'] == 0:
                        result.write("本季度从业过，则从事工作的时间不能为0\n")
            A += 1

        if psA > 0 and psB > 0:
            if hz > 1:result.write("两个以上户主？\n")
            if po > 1:result.write("户主有两个配偶？\n")
            if 1 < hzAge <= 12:result.write("户主为小孩？\n")
            if hzAge < 1:result.write("没有户主？\n")

    # result.write("ok")

# result.write(str)
    # result.write(hzAge,xb,hz,po)


if __name__ == "__main__":
    A_path = "D:/研一/项目/CheckProgram/Auditing/输入文件夹/A310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"
    zhuhu_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住户样本310151.18.csv"
    TableA = read_file(A_path)
    xiaoqu = read_file(xiaoqu_path)
    zhuhu = read_file(zhuhu_path)

    A_necessity_check(TableA,zhuhu,xiaoqu)
