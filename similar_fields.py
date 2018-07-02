#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from functions import deal_with_chinese, deal_with_number, Levenshtein
from setting import sql, cursor, db
import sys

reload(sys)
sys.setdefaultencoding('utf8')


time_start = time.time()




def deal_name(ustring):
    for ch in ustring:
        if (u'\u4e00' <= ch and ch <= u'\u9fff') or ch == u'\ue863' or ch == u"•" or ch == u"·":
            pass
        else:
            ustring = ustring.replace(ch, '')
    return ustring


def deal_chn(ustring):
    for ch in ustring:
        if u'\u4e00' <= ch and ch <= u'\u9fff':
            pass
        else:
            ustring = ustring.replace(ch, '')
    return ustring


def field_repeat_clean():
    #standard = raw_input("请输入相似度判断标准，0~1 的小数 : ")
    sql_pep_talk_1 = "select source from pep_all.pep_over GROUP BY source HAVING count(source) >1 ;"

    row = cursor.execute(sql_pep_talk_1)
    for c in cursor.fetchall():
        sql_pep_talk_2 = "select id,name,photo_img,position,purposed_position,remark from pep_all.pep_over where source='{0}'".format(
            c[0])
        row_2 = cursor.execute(sql_pep_talk_2)
        name_list = []
        name_photo_list = []
        all_list = []

        for b in cursor.fetchall():
            if not b[1]:
                a1 = '无'
            else:
                a1 = b[1]

            if not b[3]:
                a3 = '无'
            else:
                a3 = b[3]

            if not b[4]:
                a4 = '无'
            else:
                a4 = b[4]

            if not b[5]:
                a5 = '无'
            else:
                a5 = b[5]
            if not b[2]:
                a2 = '@无'   #避免有的人名字里有 “无”
                # id_name_photo_list.append(a1)
                # all_list.append(str(b[0]) + '&@#' + a1 + '&@#' + a3 + a4 + a5)
            else:
                a2 = b[2]

            name_list.append(a1)
            name_photo_list.append(a1 + a2)
            all_list.append(str(b[0]) + '&@#' + a1 + a2 + '&@#' + a3 + a4 + a5)

        result_list = Levenshtein.chongfu_list(name_photo_list)
        if result_list:
            for i in result_list:
                deal_list = []
                for j in all_list:
                    if i in j:
                        deal_list.append(j.split('&@#')[0] + '&@#' + j.split('&@#')[-1])

                print '#####################################'
                # print u'id列表',id_list
                print '\n' + u'相似度计算：'
                Levenshtein.list_str_levenshtein(deal_list)

                print '#####################################'
        else:
            print u'该source分组通过审查！(原因：主要字段不存在重复)'
        db.commit()
    # print row
    db.commit()


field_repeat_clean()
