#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import time
from functions import deal_with_chinese, deal_with_number
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db = pymysql.connect(host="localhost",user="root",password="123456",db="cnp_0522",port=3306,charset='utf8')
cursor = db.cursor()
time_start=time.time()

#数据库执行函数
def sql(sql_talk):
    try:
        row = cursor.execute(sql_talk)
        db.commit()
        print u"受影响的行数："+str(row)+u" 行  （来源:cnp数据库执行函数）"
    except:
        db.rollback()
        print u"执行错误，已经回滚，请检查数据库！"
#清理 cnp_0522_true里的 penalty_decision_date  字段
sql_talk_1=["update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'年','-');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'月','-');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'日','');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,' ','');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'\n','');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'\r','');",
"update cnp_0522.cnp_0522_true set penalty_decision_date = replace(penalty_decision_date,'\t','');"]
def clean_penalty_decision_date(sql_list):
    for s in sql_list:
        sql(s)

#查找 content=image_info 的spider(credit_lanzhou_spider、guoshui_zongju_spider)
sql_talk_2='SELECT DISTINCT spider from cnp_0522.cnp_0522_true where content=image_info;'
def content_image_info(talk):
    spider_list = []
    cursor.execute(talk)
    for spider in cursor.fetchall():
        spider_list.append(spider[0])
    return spider_list

#source content image_info 必须有一个存在
sql_talk_3='SELECT source,content,image_info,spider from cnp_0522.cnp_0522_true'
def source_content_image_info_must_one(talk):
    spider_list = []
    cursor.execute(talk)
    for spider in cursor.fetchall():
        if (spider[0] or spider[1]) or spider[2]:
            pass
        else:
            spider_list.append(spider)
    return spider_list

'''
#四码中去除无用字符（不包含中文字符）以及null
code_list_1 = ['business_registration_code','company_unified_social_credit_code','organization_code','tax_registration_code']
field_list_1=["*","/","-","--"]
def number_code_clean(code_list,field_list_1):
    for code in code_list:
        for field in field_list_1:
            sql_talk_4 = "UPDATE cnp_0522.cnp_0522_true set {0}='' where {1}='{2}'".format(code, code, field)
            print 'sql_talk: ', sql_talk_4
            try:
                row = cursor.execute(sql_talk_4)
                db.commit()
                print row
            except:
                db.rollback()

        sql_talk_4 = "UPDATE cnp_0522.cnp_0522_true set {0}='' where {1} is Null".format(code, code)
        print 'sql_talk: ', sql_talk_4
        try:
            row = cursor.execute(sql_talk_4)
            print row  # 受影响行数
            db.commit()
        except:
            db.rollback()
'''

#四码中只含有中文字符的置空
def number_code_chinese_only_clean(code_list):
    for code in code_list:
        sql_talk_4 = "select %s from cnp_0522.cnp_0522_true" % code
        print 'sql_talk: ', sql_talk_4
        try:
            row = cursor.execute(sql_talk_4)
            for c in cursor.fetchall():
                if deal_with_chinese.chinese_only(c[0]) == 1 and len(c[0]) != 0:
                    sql_talk_5 = "UPDATE cnp_0522.cnp_0522_true set {0}='' where {1} LIKE '%{2}%'".format(code, code,
                                                                                                          c[0])
                    sql(sql_talk_5)
            db.commit()
            print row
        except:
            db.rollback()

#四码中去除字符全为0的码
def number_code_zero_only_clean(code_list):
    for code in code_list:
        sql_talk_6 = "select %s,id from cnp_0522.cnp_0522_true" % code
        print 'sql_talk: ', sql_talk_6
        try:
            row = cursor.execute(sql_talk_6)
            for c in cursor.fetchall():
                if deal_with_number.zero_only(str(c[0])) and len(c[0])>0:
                    sql_talk_7 = "UPDATE cnp_0522.cnp_0522_true set {0}='' where id = '{1}'".format(code, c[1])
                    sql(sql_talk_7)
            db.commit()
            print row
        except:
            db.rollback()

#去除四码中非汉字、数字、英文字母的特殊字符
def clean_no_chi_num_char(code_list):
    for code in code_list:
        sql_talk_8 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_talk_8
        row = cursor.execute(sql_talk_8)
        for c in cursor.fetchall():
            cleaned_c = deal_with_number.clean_no_chinese_number_character(c[0])
            if cleaned_c != c[0]:
                sql_talk_9 = "UPDATE cnp_0522.cnp_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_talk_9
                sql(sql_talk_9)
        print row
        db.commit()

#标记penalty_name主体为个人的status字段为2
sql_talk_10 = 'update cnp_0522.cnp_0522_true set status = 2 WHERE char_length(penalty_name) < 4 and penalty_name RLIKE "^(赵|钱|孙|李|周|吴|郑|王|冯|陈|褚|卫|蒋|沈|韩|杨|朱|秦|尤|许|何|吕|施|张|孔|曹|严|华|金|魏|陶|姜|戚|谢|邹|喻|柏|水|窦|章|云|苏|潘|葛|奚|范|彭|郎|鲁|韦|昌|马|苗|凤|花|方|俞|任|袁|柳|酆|鲍|史|唐|费|廉|岑|薛|雷|贺|倪|汤|滕|殷|罗|毕|郝|邬|安|常|乐|于|时|傅|皮|卞|齐|康|伍|余|元|卜|顾|孟|平|黄|和|穆|萧|尹|姚|邵|湛|汪|祁|毛|禹|狄|米|贝|明|臧|计|伏|成|戴|谈|宋|茅|庞|熊|纪|舒|屈|项|祝|董|梁|杜|阮|蓝|闵|席|季|麻|强|贾|路|娄|危|江|童|颜|郭|梅|盛|林|刁|钟|徐|邱|骆|高|夏|蔡|田|樊|胡|凌|霍|虞|万|支|柯|昝|管|卢|莫|经|房|裘|缪|干|解|应|宗|丁|宣|贲|邓|郁|单|杭|洪|包|诸|左|石|崔|吉|钮|龚|程|嵇|邢|滑|裴|陆|荣|翁|荀|羊|於|惠|甄|麴|家|封|芮|羿|储|靳|汲|邴|糜|松|井|段|富|巫|乌|焦|巴|弓|牧|隗|山|谷|车|侯|宓|蓬|全|郗|班|仰|秋|仲|伊|宫|宁|仇|栾|暴|甘|钭|厉|戎|祖|武|符|刘|景|詹|束|龙|叶|幸|司|韶|郜|黎|蓟|薄|印|宿|白|怀|蒲|邰|从|鄂|索|咸|籍|赖|卓|蔺|屠|蒙|池|乔|阴|郁|胥|能|苍|双|闻|莘|党|翟|谭|贡|劳|逄|姬|申|扶|堵|冉|宰|郦|雍|舄|璩|桑|桂|濮|牛|寿|通|边|扈|燕|冀|郏|浦|尚|农|温|别|庄|晏|柴|瞿|阎|充|慕|连|茹|习|宦|艾|鱼|容|向|古|易|慎|戈|廖|庾|终|暨|居|衡|步|都|耿|满|弘|匡|国|文|寇|广|禄|阙|东|殴|殳|沃|利|蔚|越|夔|隆|师|巩|厍|聂|晁|勾|敖|融|冷|訾|辛|阚|那|简|饶|空|曾|毋|沙|乜|养|鞠|须|丰|巢|关|蒯|相|查|後|荆|红|游|竺|权|逯|盖|益|桓|公|万俟|司马|上官|欧阳|夏侯|诸葛|闻人|东方|赫连|皇甫|尉迟|公羊|澹台|公冶|宗政|濮阳|淳于|单于|太叔|申屠|公孙|仲孙|轩辕|令狐|钟离|宇文|长孙|慕容|鲜于|闾丘|司徒|司空|亓官|司寇|仉|督|子车|颛孙|端木|巫马|公西|漆雕|乐正|壤驷|公良|拓跋|夹谷|宰父|谷梁|晋|楚|闫|法|汝|鄢|涂|钦|段干|百里|东郭|南门|呼延|归|海|羊舌|微生|岳|帅|缑|亢|况|后|有|琴|梁丘|左丘|东门|西门|商|牟|佘|佴|伯|赏|南宫|墨|哈|谯|笪|年|爱|阳|佟|第五|言|福)";'
def penalty_name_persion_status_two(sql_talk):
    sql(sql_talk)

#字段全角转半角（汉字字符为全角）
def code_full_to_half(code_list):
    for code in code_list:
        sql_talk_11 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_talk_11
        row = cursor.execute(sql_talk_11)
        for c in cursor.fetchall():
            cleaned_c = deal_with_chinese.full_to_half(c[0])
            if cleaned_c != c[0]:
                sql_talk_12 = "UPDATE cnp_0522.cnp_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_talk_12
                sql(sql_talk_12)
        print row
        db.commit()

#字段penalty_decision_date规范化
def penalty_decision_date(code):
    sql_talk_13 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
    print 'sql_talk: ', sql_talk_13
    row = cursor.execute(sql_talk_13)
    for c in cursor.fetchall():
        cleaned_c = deal_with_number.deal_penalty_decision_date(c[0])
        if cleaned_c != c[0]:
            sql_talk_14 = "UPDATE cnp_0522.cnp_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c,
                                                                                                  c[1])
            print 'sql_talk: ', sql_talk_14
            sql(sql_talk_14)
    print row
    db.commit()

#高风险等级标注字段remark
sql_talk_15 = ["update cnp_0522.cnp_0522_true set status = 0, `remark` = 'High Risk' where remark is NULL and `disbelief_level` rlike '黑名单'",
"update cnp_0522.cnp_0522_true set status = 0, `remark` = 'High Risk' where remark is NULL and `penalty_results` rlike '吊销' ",
"update cnp_0522.cnp_0522_true set status = 0, `remark` = 'High Risk' where remark is NULL and  `punished_reason` rlike '偷税|漏税|虚开|违反财务报告|未按照规定报送财务|未按照规定的期限办理纳税' ",
"update cnp_0522.cnp_0522_true set status = 0, `remark` = 'High Risk' where remark is NULL and `case_nature` rlike '偷税|漏税|虚开|违反财务报告|未按照规定报送财务|未按照规定的期限办理纳税'" ]
def remark_High_Risk(sql_list):
    for s in sql_list:
        sql(s)

#三码无英文字符
def organ_tax_business_no_have_character(code_list):
    for code in code_list:
        sql_talk_16 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_talk_16
        row = cursor.execute(sql_talk_16)
        for c in cursor.fetchall():

            if deal_with_number.no_have_character_organization_business_tax(c[0]) == 'no':
                sql_talk_17 = "UPDATE cnp_0522.cnp_0522_true set {0} ='' where id = '{1}'".format(code, c[1])
                print 'sql_talk: ', sql_talk_17
                sql(sql_talk_17)
        print row
        db.commit()

#business_digits_number满足13或15位
def business_digits_number(code):

    sql_talk_18 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
    print 'sql_talk: ', sql_talk_18
    row = cursor.execute(sql_talk_18)
    for c in cursor.fetchall():

        if deal_with_number.business_registration_code_judgment(c[0]) == 'no':
            sql_talk_19 = "UPDATE cnp_0522.cnp_0522_true set {0} ='' where id = '{1}'".format(code, c[1])
            print 'sql_talk: ', sql_talk_19
            sql(sql_talk_19)
    print row
    db.commit()

#非四码清理冗余内容（包含字段开头无意义标点）
def special_character(code_list):
    for code in code_list:
        sql_talk_20 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_talk_20
        row = cursor.execute(sql_talk_20)
        for c in cursor.fetchall():
            cleaned_c = deal_with_chinese.clean_redundancy_special_character(c[0])
            if cleaned_c != c[0]:
                sql_talk_21 = "UPDATE cnp_0522.cnp_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_talk_21
                sql(sql_talk_21)
        print row
        db.commit()

#非四码清理"暂缺"、"空"、"无"、"未知"......
def clean_chinese_means_nothing(code_list):
    for code in code_list:
        sql_talk_22 = "select {0},id from cnp_0522.cnp_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_talk_22
        row = cursor.execute(sql_talk_22)
        for c in cursor.fetchall():
            if deal_with_chinese.clean_nothing_chinese(c[0]) == True:
                sql_talk_23 = "UPDATE cnp_0522.cnp_0522_true set {0} ='' where id = '{1}'".format(code, c[1])
                print 'sql_talk: ', sql_talk_23
                sql(sql_talk_23)
        print row
        db.commit()
#开始执行！

#清理 cnp_0522_true里的 penalty_decision_date  字段
clean_penalty_decision_date(sql_talk_1)

#查找 content=image_info 的spider(credit_lanzhou_spider、guoshui_zongju_spider)
s1_list=content_image_info(sql_talk_2)

#source content image_info 必须有一个存在
s2_list=source_content_image_info_must_one(sql_talk_3)

#四码中只含有中文字符的置空
four_code = ['business_registration_code','company_unified_social_credit_code','organization_code','tax_registration_code']
number_code_chinese_only_clean(four_code)

#四码中去除字符全为0的码
number_code_zero_only_clean(four_code)

#去除四码中非汉字、数字、英文字母的特殊字符
clean_no_chi_num_char(four_code)

#标记penalty_name主体为个人的status字段为2
penalty_name_persion_status_two(sql_talk_10)

#字段全角转半角（汉字字符为全角）
many_code = ['case_no','business_registration_code','company_unified_social_credit_code','organization_code','tax_registration_code','penalty_name','punished_by','punished_reason','punished_basis','legal_person','penalty_results','case_nature','penalty_decision_date','remark','content']
code_full_to_half(many_code)

#'case_no'字段去空格
#字段penalty_decision_date规范化
penalty_decision_date('penalty_decision_date')

#高风险等级标注字段remark
remark_High_Risk(sql_talk_15)

#三码无英文字符
three_code = ['business_registration_code','organization_code','tax_registration_code']
organ_tax_business_no_have_character(three_code)

#business_digits_number满足13或15位
business_digits_number('business_registration_code')

#非四码清理冗余内容（包含字段开头无意义标点）'legal_person'里面有‘*’号不要删除！
other_code=['case_no','penalty_name','punished_by','punished_reason','punished_basis','penalty_results','case_nature','remark','content']
special_character(other_code)

#非四码意为无或无意义的字符
clean_chinese_means_nothing(other_code)

for s1 in s1_list:
    print u"content=image_info 的spider: "+s1

for s2 in s2_list:
    print u"source content image_info都不存在: "+s2



'''
#case_no  个别开头为‘(’误删恢复
sql_talk_20 = "select case_no,id from cnp_0522.cnp_0522_true WHERE case_no is not null and case_no !=''"
print 'sql_talk: ', sql_talk_20
row = cursor.execute(sql_talk_20)
for c in cursor.fetchall():
    if c[0][0]>=u'\u0030' and c[0][0]<=u'\u0039':
        cleaned_c = "("+c[0]

        sql_talk_21 = "UPDATE cnp_0522.cnp_0522_true set case_no ='{0}' where id = '{1}'".format( cleaned_c, c[1])
        print 'sql_talk: ', sql_talk_21
        sql(sql_talk_21)
print row
db.commit()
'''
time_end=time.time()
print u"程序运行时间："+str(time_end-time_start)+u'秒'