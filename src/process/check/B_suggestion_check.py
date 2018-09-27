# ********************************
# *   全国住户生活状况调查季报   *
# *    问卷B审核公式（必要性）   *
# *        2015年08月26日        *
# ********************************
import pandas as pd
import datetime

Year = datetime.datetime.now().year
Month = datetime.datetime.now().month

result = open(r'D:\研一\审核程序\src\审核结果输出\B_suggestion_Check_result.txt', 'w')


def read_file(path):
    return pd.read_csv(path, header=0)


def B_suggestion_check(tableB):
    B, M = 92, 993
    E = 95
    # if M_91 == M_94:  #//开户拒访：开户时间和拒访时间相同
    # if table['M91'] == table['M94']:
    # nextHousehold

    M_path = "D:\研一\审核程序\src\输入文件夹\M310151.摸底.csv"
    fp3 = open(M_path)
    tableM = read_file(fp3)

    E_path = "D:\研一\审核程序\src\输入文件夹\E310151.开户.csv"
    fp4 = open(E_path)
    tableE = read_file(fp4)

    # B1部分    住房基本情况
    # B1.1    期末现住房基本情况
    result.write(tableB['SID']+': ')
    if pd.isnull(tableB['B101']) == False:
        # 逻辑审核
        if tableB['B103'] == 4:
            if tableB['B102'] != 2 and tableB['B102'] != 7 and tableB['B102'] != 8:
                result.write('竹草土坯结构的房屋是楼房或单元房吗？请核实')

    for index, Modi in tableM.iterrows():
        if tableB['SID'][:-2] == Modi['SID']:
            if Modi['M101'] == 1 and pd.isnull(tableB['B101'])==False:
                # B1.2自有现住房情况
                if tableB['B104'] >= 3 and tableB['B104'] <= 8:
                    if tableB['B117'] < 1949 or tableB['B117'] > Year * 100 + Month:
                        result.write('B117自有现住房建筑年份越界')
                    if tableB['B118'] / 100 > tableB['B121']:
                        result.write('自有现住房现市场价是原购建价的100倍以上，请核实')
                    if tableB['B103'] == 4:
                        if tableB['B117'] < 1970:
                            result.write('请核实竹草土坯结构房屋的建筑年份')
                        if tableB['B118'] > 10:
                            result.write('请核实竹草土坯结构房屋的市场价值')
                    if pd.isnull(tableB['B105']) == False:
                        if tableB['B118'] / tableB['B105'] <= 0.01 or tableB['B118'] / tableB['B105'] >= 8:
                            # print(tableB['B118'] / tableB['B105'])
                            result.write('B118 自有现住房单价越界,请核实')
                # B1.3租赁房实际月租金
                if tableB['B104'] == 1:
                    if Modi['M101'] < 2 and Modi['M205'] != 4:
                        if tableB['B127'] > 0:
                            if tableB['B127'] < 10 or tableB['B127'] >= 999:
                                result.write('B127租赁公房实际月租金越界')
                if tableB['B104'] == 2:
                    if Modi['M101'] < 2 and Modi['M205'] != 4:
                        if tableB['B127'] > 0:
                            if tableB['B127'] < 100 or tableB['B127'] >= 9999:
                                result.write('B127租赁私房实际月租金越界')

                # B1.4期内拥有其他房屋情况
                if tableB['B131'] > 0:
                    if tableB['B133'] < 10 or tableB['B133'] >= 9999:
                        result.write('B133出租商用建筑物月租金越界')
                # 出租屋单间越界
                if tableB['B128'] > 0:
                    if tableB['B129'] / tableB['B128'] <= 0.1 or tableB['B129'] / tableB['B128'] >= 8:
                        result.write('出租住房单价越界,请核实')
                if tableB['B131'] > 0:
                    if tableB['B132'] / tableB['B131'] <= 0.1 or tableB['B132'] / tableB['B131'] >= 8:
                        result.write('出租商用建筑物单价越界，请核实')
                if tableB['B134'] > 0:
                    if tableB['B135'] / tableB['B134'] <= 0.1 or tableB['B135'] / tableB['B134'] >= 8:
                        result.write('偶尔居住房单价越界，请核实')
                if tableB['B136'] > 0:
                    if tableB['B137'] / tableB['B136'] <= 0.1 or tableB['B137'] / tableB['B136'] >= 8:
                        result.write('空宅或其他用途住房单价越界,请核实')

                # B1.5新购住房情况审核
                if tableB['B104'] >= 4 and tableB['B104'] <= 7 and tableB['B120'] <= 2019:
                    if tableB['B139'] < 0 or tableB['B139'] >= 999:
                        result.write('新购住房总金额越界')
                    if tableB['B138'] != 0:
                        if tableB['B139'] / tableB['B138'] <= 0.1 or tableB['B138'] / tableB['B137'] >= 8:
                            result.write('新购住房单价越界，请核实')

                # B1.6新建住房情况审核
                if tableB['B104'] == 3 and tableB['B120'] == Year:
                    if tableB['B144'] != 0:
                        if tableB['B145'] < 0.1 or tableB['B145'] >= 999:
                            result.write('新建住房总费用越界')
                        if tableB['B145'] / tableB['B144'] <= 0.01 or tableB['B145'] / tableB['B144'] >= 3:
                            result.write('新建住房单价越界，请核实')
                    if tableB['B145'] < 0.5 or tableB['B145'] >= 999:
                        result.write('B145购（建）房总金额越界')
                # B1.7期内住房大修或装修费用
                if tableB['B150'] > 99:
                    result.write('住房大修或专修费用越界')

    # B3部分 年末粮食结存
    # if TaskCode == 7 and pd.isnull(tableB['B101']) == False:
    if pd.isnull(tableB['B101']) == False:
        if tableB['B230'] + tableB['B231'] + tableB['B232'] + tableB['B233'] + tableB['B234'] + tableB['B235'] + tableB['B236'] + tableB['B237'] < 0:
            result.write('没有粮食结存，请核实')
        for index2, kaihu in tableE.iterrows():
            if kaihu['SID'] == tableB['SID']:
                if kaihu['E113'] > 0:
                    if tableB['B230'] + tableB['B231'] <= 0:
                        result.write('有种植小麦，但无小麦或面粉结存，请核实')
                if kaihu['E114'] > 0:
                    if tableB['B232'] + tableB['B233'] <= 0:
                        result.write('有种植水稻，但无稻谷或大米结存，请核实')
                if kaihu['E115'] > 0:
                    if tableB['B234'] + tableB['B235'] <= 0:
                        result.write('有种植玉米。但无玉米或玉米面结存，请审核')
                if kaihu['E116'] + kaihu['E117'] > 0:
                    if tableB['B236'] + tableB['B237'] <= 0:
                        result.write('有种植大豆或薯类，但无其他原粮或加工粮结存，请审核')

    # B3部分 补充资料3：家庭或家庭成员合伙、参股或独立控股公司（企业）
    # if (tableB['B101'])
    if pd.isnull(tableB['B101']) == False:
        if tableB['B242'] < 0 or tableB['B242'] > 5000:
            result.write('公司（企业）税后净利润可能偏高，请核实')
        if tableB['B244'] < 0 or tableB['B244'] > 500:
            result.write('属于本住户或住户成员名下股份的公司（企业）税后净利润可能偏高，请核实')

    result.write('\n')

if __name__ == "__main__":
    path = " "
    df = read_file("D:\研一\审核程序\src\输入文件夹\B310151.18.csv")
    print(df.index)
    i = 2
    # result.write(df)
    for row in df.iterrows():
        result.write('第%d行数据：\n' % i)
        i += 1
        B_suggestion_check(row[1])
        # result.write(row[1]["A101"])
        result.write('\n')
    result.close()