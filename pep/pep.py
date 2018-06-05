#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import time
from functions import deal_with_chinese, deal_with_number
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db = pymysql.connect(host="localhost",user="root",password="123456",db="pep_0522",port=3306,charset='utf8')
cursor = db.cursor()
time_start=time.time()

#数据库执行函数
def sql(sql_talk):
    try:
        row = cursor.execute(sql_talk)
        db.commit()
        print u"受影响的行数："+str(row)+u" 行  （来源:pep数据库执行函数）"
    except:
        db.rollback()
        print u"执行错误，已经回滚，请检查数据库！"


#删除no重复的
sql_pep_talk_1="select id from pep_0522.pep_0522_true where no in (select no FROM pep_all.pep_all)"
def delete_no_repeat(sql_talk):
    print 'sql_talk: ', sql_pep_talk_1
    row = cursor.execute(sql_pep_talk_1)
    for c in cursor.fetchall():
        sql_pep_talk_2 = "DELETE FROM pep_0522.pep_0522_true WHERE id = '{0}'".format(c[0])
        print 'sql_talk: ', sql_pep_talk_2
        sql(sql_pep_talk_2)
    print row
    db.commit()

#字段全角转半角（汉字字符为全角）
all_code_list=['name','gender','birth','position','purposed_position','ethnicity','place_of_birth','remark']
def code_full_to_half(code_list):
    for code in code_list:
        sql_pep_talk_3 = "select {0},id from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_pep_talk_3
        row = cursor.execute(sql_pep_talk_3)
        for c in cursor.fetchall():
            cleaned_c = deal_with_chinese.full_to_half(c[0])
            if cleaned_c != c[0]:
                sql_pep_talk_4 = "UPDATE pep_0522.pep_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_pep_talk_4
                sql(sql_pep_talk_4)
        print row
        db.commit()

#清洗remark字段里的英文、非，。：-的字符
def clean_remark(code):
    sql_pep_talk_4 = "select {0},id from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
    print 'sql_talk: ', sql_pep_talk_4
    row = cursor.execute(sql_pep_talk_4)
    for c in cursor.fetchall():
        cleaned_c = deal_with_chinese.clean_pep_remark(c[0])
        if cleaned_c != c[0]:
            sql_pep_talk_5 = "UPDATE pep_0522.pep_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
            print 'sql_talk: ', sql_pep_talk_5
            sql(sql_pep_talk_5)
    print row
    db.commit()

#清洗pep name\gender\ethnicity\place_of_birth
four_code_list=['name','gender','ethnicity','place_of_birth']
def clean_pep_name_gender_ethnicity_place_of_birth(code_list):
    for code in code_list:
        sql_pep_talk_6 = "select {0},id from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_pep_talk_6
        row = cursor.execute(sql_pep_talk_6)
        for c in cursor.fetchall():
            cleaned_c = deal_with_chinese.clean_pep_n_g_e_p(c[0])
            if cleaned_c != c[0]:
                sql_pep_talk_7 = "UPDATE pep_0522.pep_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_pep_talk_7
                sql(sql_pep_talk_7)
        print row
        db.commit()

#名字name有问题的spider记录
def name_problem_spider(code):
    spider_list=[]
    sql_pep_talk_8 = "select {0},spider from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code, code,
                                                                                                           code)
    print 'sql_talk: ', sql_pep_talk_8
    row = cursor.execute(sql_pep_talk_8)
    for c in cursor.fetchall():
        if (len(c[0])<2 or len(c[0])>5) and u"·" not in c[0]:
            if c[1] in spider_list:
                pass
            else:
                spider_list.append(c[1])
    print row
    db.commit()
    return spider_list

#民族字段问题
def deal_ethnicity_problem(code):
    sql_pep_talk_9 = "select {0},id from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code, code,
                                                                                                           code)
    print 'sql_talk: ', sql_pep_talk_9
    row = cursor.execute(sql_pep_talk_9)
    for c in cursor.fetchall():
        cleaned_c = deal_with_chinese.deal_ethnicity_field(c[0])
        if cleaned_c != c[0]:
            sql_pep_talk_10 = "UPDATE pep_0522.pep_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c,
                                                                                                    c[1])
            print 'sql_talk: ', sql_pep_talk_10
            sql(sql_pep_talk_10)
    print row
    db.commit()

#多个字段去空格、换行符等
def clean_many_field_space_newline(code_list):
    for code in code_list:
        sql_pep_talk_11 = "select {0},id from pep_0522.pep_0522_true WHERE {1} is not null and {2} !=''".format(code,code,code)
        print 'sql_talk: ', sql_pep_talk_11
        row = cursor.execute(sql_pep_talk_11)
        for c in cursor.fetchall():
            cleaned_c = c[0].replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace(u'\u3000','').replace(u'\xa0','')
            if cleaned_c != c[0]:
                sql_pep_talk_12 = "UPDATE pep_0522.pep_0522_true set {0} ='{1}' where id = '{2}'".format(code, cleaned_c, c[1])
                print 'sql_talk: ', sql_pep_talk_12
                sql(sql_pep_talk_12)
        print row
        db.commit()
'''
#删除no重复的
delete_no_repeat(sql_pep_talk_1)
#字段全角转半角（汉字字符为全角）
code_full_to_half(all_code_list)
#清洗remark字段里的英文、非，。：-的字符
clean_remark('remark')
#清洗pep name\gender\ethnicity\place_of_birth
clean_pep_name_gender_ethnicity_place_of_birth(four_code_list)
#名字name有问题的spider记录
for s in name_problem_spider('name'):
    print s
#民族字段
deal_ethnicity_problem('ethnicity')
#多个字段空格
clean_many_field_space_newline(all_code_list)
'''

time_end=time.time()
print u"程序运行时间："+str(time_end-time_start)+u'秒'