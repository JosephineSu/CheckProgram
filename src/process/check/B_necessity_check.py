# ********************************
# *   全国住户生活状况调查季报   *
# *    问卷B审核公式（必要性）   *
# *        2015年08月26日        *
# ********************************
import pandas as pd
import datetime

Year = datetime.datetime.now().year
Month = datetime.datetime.now().month
# global i = 2
result = open(r'D:\研一\审核程序\src\审核结果输出\B_necessity_CheckResult.txt','w')

def read_file(path):
    return pd.read_csv(path, header=0)

def B_necessity_check(tableB):
    B,M = 92,993
    E = 95
    M_path = "D:\研一\审核程序\src\输入文件夹\M310151.摸底.csv"
    fp3 = open(M_path)
    tableM = read_file(fp3)
    #if M_91 == M_94:  #//开户拒访：开户时间和拒访时间相同
    #if tableB['M91'] == tableB['M94']:
     #   nextHousehold

    # B1部分    住房基本情况
    #B1.1    期末现住房基本情况
    #超界错误。b101 - b116重写，0825lw
    #B101 ?: "B101填报错误"
    #if tableB['B101']:
    result.write(tableB['SID']+': ')
    if pd.isnull(tableB['B101']) == False:
        # print('aaaa')
        if tableB['B101'] < 1 or tableB['B101'] > 4:
            result.write('住宅类型越界，请填写（1-4）')
        if tableB['B102'] < 1 or tableB['B102'] > 8:
            result.write('本住宅的建筑样式越界，请填写（1-8）')
        if tableB['B103'] < 1 or tableB['B103'] > 5:
            result.write('主要建筑材料越界，请填写（1-5）')
        if tableB['B104'] < 1 or tableB['B104'] > 11:
            result.write('房屋来源越界，请填写（1-11）')
        if tableB['B105'] <= 0 or tableB['B105'] > 999:
            result.write('建筑面积填报越界，请核实')
        if tableB['B106'] <1 or tableB['B106'] > 3:
            result.write('住宅外道路路面情况越界，请填写（1-3）')
        if tableB['B107'] <1 or tableB['B107'] > 3:
            result.write('住宅内是否有管道自来水越界，请填写（1-3）')
        if tableB['B108'] < 1 or tableB['B108'] > 7:
            result.write('主要饮用水来源越界，请填写（1-7））')
        if tableB['B109'] < 1 or tableB['B109'] > 4:
            result.write('获取饮用水存在的困难越界，请填写（1-4）')
        if tableB['B110'] < 1 or tableB['B110'] > 5:
            result.write('饮用水处理措施越界，请填写（1-5）')
        if tableB['B111'] < 1 or tableB['B111'] > 5:
            result.write('厕所类型越界，请填写（1-5）')
        if tableB['B112'] < 1 or tableB['B112'] > 3:
            result.write('厕所使用情况越界，请填写（1-3）')
        if tableB['B113'] < 1 or tableB['B113'] > 4:
            result.write('洗澡设施越界，请填写（1-4）')
        if tableB['B114'] < 1 or tableB['B114'] > 3:
            result.write('主要取暖设备状况越界，请填写（1-3）')
        if tableB['B115'] < 1 or tableB['B115'] > 11:
            result.write('主要取暖能源状况越界，请填写（1-11）')
        if tableB['B116'] < 1 or tableB['B116'] > 11:
            result.write('主要灶用能源状况越界，请填写（1-11）')

        # #住家保姆、帮工或者集体居住户审核
        # if tableM['M205'] == 4:
        #     for i in range(tableB['B117'],tableB['B150']):
        #         if i != 0:
        #             result.write('住家保姆、帮工,不用填B117-B150')
        # if tableM['M205'] == 4 and tableB['B101'] != 4:
        #     result.write('住家保姆、帮工,B101要填4')
        # if tableM['M205'] == 4 and tableB['B104'] != 10:
        #     result.write('住家保姆、帮工,B104要填10')
        # if tableM['M205'] == 4 and tableB['B112'] != 2:
        #     result.write('住家保姆、帮工,B112要填2')

        #逻辑审核
        if tableB['B102'] == 8:
            if tableB['B103'] == 1 or tableB['B103'] == 2:
                result.write('居住空间样式为其他，建筑材料不应为钢混或砖混结构')
        if tableB['B107'] == 1 and tableB['B109'] == 1:
            result.write('有自来水，单次取水时间却超过半小时？')

        #跳转审核
        if tableB['B104'] >= 3 and tableB['B104'] <= 8:
            if tableB['B117']+tableB['B118']+tableB['B119']+tableB['B120']+tableB['B121']+tableB['B122']+tableB['B123']+tableB['B124']+tableB['B125']+tableB['B126']<= 0:
                result.write('现住房为自有房者应填写B117-B126')
        # if tableB['B104'] == 1 or tableB['B104'] == 2:
        #     if tableM['M101'] <= 1 and tableM['M205'] == 4:
        #         if tableB['B127'] <= 0:
        #             result.write('现住房为租赁房者应填写B127')
        if tableB['B104'] == 1 or tableB['B104'] == 2:
            for i, Modi in tableM.iterrows():
                if Modi['M101'] <= 1 and Modi['M205'] == 4:
                    if tableB['B127'] <= 0:
                        result.write('现住房为租赁房者应填写B127')
    # print('ok')
    for index, Modi in tableM.iterrows():
        if tableB['SID'][:-2] == Modi['SID']:
            # print(tableB['SID'][:-2],Modi['SID'])
            # print ('bbbb')
            if pd.isnull(tableB['B101']) == False:
                # 住家保姆、帮工或者集体居住户审核
                if Modi['M205'] == 4:
                    for i in range(tableB['B117'], tableB['B150']):
                        if i != 0:
                            result.write('住家保姆、帮工,不用填B117-B150')
                if Modi['M205'] == 4 and tableB['B101'] != 4:
                    result.write('住家保姆、帮工,B101要填4')
                if Modi['M205'] == 4 and tableB['B104'] != 10:
                    result.write('住家保姆、帮工,B104要填10')
                if Modi['M205'] == 4 and tableB['B112'] != 2:
                    result.write('住家保姆、帮工,B112要填2')

            if Modi['M101'] == 1 and pd.isnull(tableB['B101']) == False:
                #B1.2 自有现住房情况
                if tableB['B104'] >= 3 and tableB['B104'] <= 8:
                    if tableB['B118'] < 0.5 or tableB['B118'] >= 999:
                        result.write('B118自有现住房市场价越界')
                    if tableB['B119'] < 100 or tableB['B119'] >= 9999:
                        result.write('B119同类住房的市场价月租金越界')
                    if tableB['B120'] < 1949 or tableB['B120'] > Year:
                        result.write('B120现住房购(建)房时间越界')
                    if tableB['B121'] < 0.5 or tableB['B121'] >= 999:
                        result.write('B121购(建)房总金额越界')
                    if tableB['B122']!=0 :
                        if tableB['B122'] < 0.1 or tableB['B122'] >= 999:
                            result.write('B122购(建)房时借贷总额(不含利息)越界')
                        if tableB['B125'] < 1 or tableB['B125'] > 30:
                            result.write('B125借贷款还款总年限越界')
                    if pd.isnull(tableB['B123']) == False:
                        if tableB['B123'] < 1 or tableB['B123'] >= 999:
                            result.write('B123购(建)房按揭贷款越界')
                    if pd.isnull(tableB['B124']) == False:
                        if tableB['B124'] < 0.01 or tableB['B124'] >= 99:
                            result.write('B124购(建)房时借贷款总利息越界')
                    if pd.isnull(tableB['B125']) == False:
                        if tableB['B126'] != 1 and tableB['B126'] != 2:
                            result.write('B126现在是否还在还款越界')
                    if tableB['B121'] < tableB['B122']:
                        result.write('借贷款总额不应大于购(建)房总金额')
                    if tableB['B122'] < tableB['B123']:
                        result.write('按揭贷款不应大于借贷款总额')
                    if tableB['B122'] == 0:
                        if pd.isnull(tableB['B124'])== False:
                            result.write('没借贷款不应有利息')
                        if pd.isnull(tableB['B125'])== False:
                            result.write('没借贷款不应填还款总年限')
                        if pd.isnull(tableB['B126'])== False:
                            result.write('没借贷款不应填写B126')
                #B1.3 期内拥有其它房屋情况
                if tableB['B128'] > 0:
                    if tableB['B128'] < 5 or tableB['B128'] > 999:
                        result.write('B128出租住房建筑面积填报越界')
                    if tableB['B129'] < 0.3 or tableB['B129'] >= 999:
                        result.write('B129出租住房市场价越界')
                    if tableB['B130'] < 100 or tableB['B130'] >= 9999:
                        result.write('B130出租住房月租金越界')
                if tableB["B131"] > 0:
                    if tableB['B131'] < 1 or tableB['B131'] > 999:
                        result.write('B131出租商用建筑物建筑面积填报越界')
                    if tableB['B132'] < 0.3 or tableB['B132'] >= 999:
                        result.write('B132出租商用建筑物市场价越界')
                if tableB["B134"] > 0:
                    if tableB['B134'] < 1 or tableB['B134'] > 999:
                        result.write('B134偶尔居住房建筑面积填报越界')
                    if tableB['B135'] < 0.3 or tableB['B135'] >= 999:
                        result.write('B135偶尔居住房市场价越界')
                if tableB["B136"] > 0:
                    if tableB['B136'] < 1 or tableB['B136'] > 999:
                        result.write('B136空宅或其他用途住房建筑面积填报越界')
                    if tableB['B137'] < 0.3 or tableB['B137'] >= 999:
                        result.write('B137空宅或其他用途住房市场价越界')

                #B1.4新购住房情况审核
                if tableB['B104'] >= 4 and tableB['B104'] <= 7 and tableB['B120'] == Year:
                    if tableB['B138'] < 5 or tableB['B138'] >= 999:
                        result.write('新购住房建筑面积越界')
                    if tableB['B140'] != 0:
                        if tableB['B140'] < 1 or tableB['B140'] >= 999:
                            result.write('新购住房借贷款总额(不含利息)越界')
                        if tableB['B141'] < 1 or tableB['B141'] >= 999:
                            result.write('新购住房按界揭贷款越')
                        if tableB['B142'] < 1 or tableB['B142'] >= 99:
                            result.write('新购住房借贷款总利息越界')
                        if tableB['B143'] < 1 or tableB['B143'] > 30:
                            result.write('新购住房借贷款还款总年限越界')
                        if tableB['B142']/tableB['B140'] < 0 or tableB['B142']/tableB['B140'] >= 0.15:
                            result.write('贷款利率越界')
                        if tableB['B143'] < 3 or tableB['B143'] > 30:
                            result.write('还款年限越界')
                    if tableB['B139'] <= tableB['B140']:
                        result.write('借贷款总额不应大于购(建)房总金额')
                    if tableB['B140'] < tableB['B141']:
                        result.write('按揭贷款不应大于借贷款总额')
                    if tableB['B140'] == 0:
                        if tableB['B142'] !=0:
                            result.write('没借贷款不应有利息')
                        if tableB['B143'] != 0:
                            result.write('没借贷款不应填还款总年限')

                #B1.5 新住房情况审核
                if tableB['B104'] == 3 and tableB['B120'] == Year:
                    if tableB['B144'] != 0:
                        if tableB['B144'] < 5 or tableB['B144'] >= 999:
                            result.write('新住房建筑面积越界')
                    if tableB['B145'] != tableB['B146'] + tableB['B147'] + tableB['B148'] + tableB['B149']:
                        result.write('建房资金来源不平')

                #B1.6 期内住房大修或装修费用
                if tableB['B150'] > 99:
                    result.write('住房大修或装修费用越界')

    #B2部分 耐用消费品情况
    # if tableB['B101']:
    if pd.isnull(tableB['B101']) == False:
        # print('ccc')
        if tableB['B201'] < 0 or tableB['B201'] > 3:
            result.write('B201耐用消费品拥有量超界，请核实')
        if tableB['B202'] < 0 or tableB['B202'] > 3:
            result.write('B202耐用消费品拥有量超界，请核实')
        if tableB['B203'] < 0 or tableB['B203'] > 5:
            result.write('B203耐用消费品拥有量超界，请核实')
        if tableB['B204'] < 0 or tableB['B204'] > 5:
            result.write('B204耐用消费品拥有量超界，请核实')
        if tableB['B205'] < 0 or tableB['B205'] > 5:
            result.write('B205耐用消费品拥有量超界，请核实')
        if tableB['B206'] < 0 or tableB['B206'] > 5:
            result.write('B206耐用消费品拥有量超界，请核实')
        if tableB['B207'] < 0 or tableB['B207'] > 5:
            result.write('B207耐用消费品拥有量超界，请核实')
        if tableB['B208'] < 0 or tableB['B208'] > 10:
            result.write('B208耐用消费品拥有量超界，请核实')
        if tableB['B209'] < 0 or tableB['B209'] > 7:
            result.write('B209耐用消费品拥有量超界，请核实')
        if tableB['B210'] < 0 or tableB['B210'] > 3:
            result.write('B210耐用消费品拥有量超界，请核实')
        if tableB['B211'] < 0 or tableB['B211'] > 5:
            result.write('B211耐用消费品拥有量超界，请核实')
        #if tableB['B212'] < 0 or tableB['B212'] > 5:
         #   result.write('B212耐用消费品拥有量超界，请核实')
        if tableB['B213'] < 0 or tableB['B213'] > 2:
            result.write('B213耐用消费品拥有量超界，请核实')
        if tableB['B214'] < 0 or tableB['B214'] > 2:
            result.write('B214耐用消费品拥有量超界，请核实')
        if tableB['B215'] < 0 or tableB['B215'] > 3:
            result.write('B215耐用消费品拥有量超界，请核实')
        if tableB['B216'] < 0 or tableB['B216'] > 10:
            result.write('B216耐用消费品拥有量超界，请核实')
        if tableB['B217'] < 0 or tableB['B217'] > 10:
            result.write('B217耐用消费品拥有量超界，请核实')
        if tableB['B218'] < 0 or tableB['B218'] > 10:
            result.write('B218耐用消费品拥有量超界，请核实')
        if tableB['B219'] < 0 or tableB['B219'] > 10:
            result.write('B219耐用消费品拥有量超界，请核实')
        #if tableB['B220'] < 0 or tableB['B220'] > 5:
         #   result.write('B220耐用消费品拥有量超界，请核实')
        if tableB['B221'] < 0 or tableB['B221'] > 5:
            result.write('B221耐用消费品拥有量超界，请核实')
        if tableB['B222'] < 0 or tableB['B222'] > 5:
            result.write('B222耐用消费品拥有量超界，请核实')
        if tableB['B223'] < 0 or tableB['B223'] > 5:
            result.write('B223耐用消费品拥有量超界，请核实')
        #if tableB['B224'] < 0 or tableB['B224'] > 5:
         #   result.write('B224耐用消费品拥有量超界，请核实')
        if tableB['B225'] < 0 or tableB['B225'] > 5:
            result.write('B225耐用消费品拥有量超界，请核实')
        if tableB['B226'] < 0 or tableB['B226'] > 5:
            result.write('B226耐用消费品拥有量超界，请核实')
        if tableB['B208'] > tableB['B207']:
            result.write('B208拥有量不应超过B207，请核实')
        if tableB['B211'] > tableB['B210']:
            result.write('B211拥有量不应超过B210，请核实')
        if tableB['B217'] > tableB['B216']:
            result.write('B217拥有量不应超过B216，请核实')
        if tableB['B219'] > tableB['B218']:
            result.write('B219拥有量不应超过B218，请核实')

    #B3部分 补充资料2：现住房房屋状况
    # if tableB['B101']:
        if tableB['B238'] < 1 or tableB['B238'] > 4:
            result.write('住户现住房所处场地状况越界，请填写(1-4)')
        if tableB['B239'] < 1 or tableB['B239'] > 4:
            result.write('住户现住房屋安全状况越界，请填写(1-4)')
        if tableB['B240'] != 1 and tableB['B240'] != 2:
            result.write('住宅地面是否经常有泥土、沙土、畜禽粪便等脏东西越界，请填写(1-2)')

    #B3部分 补充资料3：家庭或家庭成员合伙、参股或独立控股公司（企业）的经营情况 *     lw 0905
    # if tableB['B101']:
        if tableB['B241'] != 1 and tableB['B241'] != 2:
            result.write('是否拥有独立控股的公司（企业）越界，请填写(1-2)')
        if tableB['B243'] != 1 and tableB['B243'] != 2:
            result.write('是否拥有合伙或参股的公司（企业）越界，请填写(1-2)')
        if tableB['B242'] > 0:
            if tableB['B241'] != 1:
                result.write('有公司（企业）税后净利润，应有公司')
        if tableB['B244'] > 0:
            if tableB['B243'] != 1:
                result.write('有公司（企业）税后净利润，应有公司')

    result.write('\n')
    # print('done!')


if __name__ == "__main__":
    B_path = "D:\研一\审核程序\src\输入文件夹\B310151.18.csv"
    fp2 = open(B_path)
    tableB = read_file(fp2)
    # M_path = "D:\研一\审核程序\src\输入文件夹\M310151.摸底.csv"
    # fp3 = open(M_path)
    # tableM = read_file(fp3)
    #df = read_file("G:/testData/B310151.18.csv")
    #print(df.index)
    print(tableB.index)
    i = 2
    # result.write(df)
    for row in tableB.iterrows():
        result.write('第%d行数据：\n'%i)
        i += 1
        B_necessity_check(row[1])
        # result.write(row[1]["A101"])
        result.write('\n')
    result.close()