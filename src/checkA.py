#A问卷外部审核

import pandas as pd
import datetime

result = open(r'D:\研一\项目\CheckProgram\Auditing\输出结果\IndependentCheckAResult.txt','w')

def read_file(path):
    return pd.read_csv(path, header=0, encoding='gbk')

def A_independent_check(hu_data)
    M_path = M_path = "D:\研一\审核程序\src\输入文件夹\M310151.摸底.csv"
    fp3 = open(M_path)
    tableM = read_file(fp3)

    for index1,tableA in hu_data.iterrows():
        result.write(tableA['A101']+ "\n")
        if tableA['A108'] == 6:
            result.write('A108=6，户口登记地在省外，应直接填写省代码\n')
        if tableA['A108'] == 7:
            result.write('A108=7，户口登记地为其他？请核实\n')
        if tableA['A106'] >= 16 and tableA['A112'] == 3 and tableA['A203'] == 2:
            if tableA['A111'] == 4:
                result.write('A111确实是公费医疗？请核实并注明具体情况\n')
            # ("1"$a202 and not "1"$a111) or ("2"$a202 and not "2"$a111) or ("3"$a202 and not "3"$a111)
            # ("4"$a202 and not "5"$a111) or ("5"$a202 and not "6"$a111)
            #     result.write('A111医疗保险种类与A202养老保险不一致，请核实')
            pk1 = tableA['A111'] == 1 and tableA['202'] != 1
            pk2 = tableA['A111'] == 2 and tableA['202'] != 2
            pk3 = tableA['A111'] == 3 and tableA['202'] != 3
            pk4 = tableA['A111'] != 1 and tableA['202'] == 1
            pk5 = tableA['A111'] != 2 and tableA['202'] == 2
            pk6 = tableA['A111'] != 3 and tableA['202'] == 3
            if pk1 or pk2 or pk3 or pk4 or pk5 or pk6:
                result.write('A111医疗保险种类与A202养老保险不一致，请核实\n')

        if len(tableA['A108'].strip(' ')) > 1 and tableA['A204'] == 1 :
            if tableA['A111'] == 7:
                result.write('外来务工人员，未参加任何医疗保险A111=7，请核实并注明具体情况\n')
            if tableA['A202'] == 6:
                result.write('外来务工人员，未参加任何养老保险A202=6，请核实并注明具体情况\n')

        df = tableM[tableA['SID'][:-2] == tableM['SID']]
        for index2,tableAM in df.iterrows():
            if tableAM['M217'] == 1:
                if tableAM['A201'] == 1 or tableAM['A201'] == 2 and tableAM['A202'] == 6:
                    result.write(tableAM['A101']+':具体情况]\n')

if __name__ == '__main__':
