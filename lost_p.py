#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
db = pymysql.connect(host="localhost", user="root", password="123456", db="sun", port=3306, charset='utf8')
cursor = db.cursor()
# 数据库执行函数
def sql(sql_talk):
    try:
        row = cursor.execute(sql_talk)
        db.commit()
        print sql_talk
        print u"受影响的行数：" + str(row) + u" 行  （来源:pep数据库执行函数）"
    except:
        db.rollback()
        print u"执行错误，已经回滚，请检查数据库！"

def md5(string):
    m = hashlib.md5()
    if type(string) == str:
        m.update(string)
        return m.hexdigest()
    else:
        m.update(string.encode('utf-8'))
        return m.hexdigest()


'''
sql_talk_company = "select name,code,legal_person,execute_court,area,basis_no,record_time,case_no,punished_by,legal_obligations,fulfill,behavior,publish_time from sun.lost_promise_company"
row = cursor.execute(sql_talk_company)
for c in cursor.fetchall():
    text_company =  '被执行人姓名/名称：'+c[0]+'\n'+'身份证号码/组织机构代码：'+c[1]+'\n'+'法定代表人或者负责人姓名：'+c[2]+'\n'+'执行法院：'+c[3]+'\n'+'省份：'+c[4]+'\n'+'执行依据文号：'+c[5]+'\n'+'立案时间：'+c[6]+'\n'+'案号：'+c[7]+'\n'+'做出执行依据单位：'+c[8]+'\n'+'生效法律文书确定的义务：'+c[9]+'\n'+'被执行人的履行情况：'+c[10]+'\n'+'失信被执行人行为具体情形：'+c[11]+'\n'+'发布时间：'+c[12]
    sql_talk_update_company = "update sun.lost_promise_company set content='{0}';".format(text_company)
    sql(sql_talk_update_company)
db.commit()
print row

sql_talk_personal = "select * from sun.lost_promise_company"
row = cursor.execute(sql_talk_personal)
for c in cursor.fetchall():
    sql_talk_update_personal = "insert into sun.cn_punishments_org set no='{0}',case_no='{1}' ,penalty_name='{2}',punished_by='{3}',punished_reason='{4}',penalty_decision_date='{5}',source='{6}',content='{7}',image_info='{8}',modified='{9}',spider='shixin_court_spider',http_method='GET',organization_code='{10}',legal_person='{11}';".format(c[19],c[13],c[16],c[5],c[22],c[12],c[10],c[9],c[1],c[20],c[2],c[11])
    sql(sql_talk_update_personal)
    #print c
db.commit()
print row   
##############
sql_talk_personal = "select * from sun.cn_punishments_ind"
row = cursor.execute(sql_talk_personal)
for c in cursor.fetchall():
    m = md5(c[3]+c[11]+c[21])
    sql_talk_update_personal = "update sun.cn_punishments_ind set no='{0}' where id ='{1}';".format(m,c[0])
    sql(sql_talk_update_personal)
    #print len(c)
db.commit()
print row
'''
