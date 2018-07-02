#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

import sys

reload(sys)
sys.setdefaultencoding('utf8')

db = pymysql.connect(host="localhost", user="root", password="123456", db="pep_all", port=3306, charset='utf8')
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
