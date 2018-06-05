#! /usr/bin/env python
# -*- coding: utf-8 -*-
from deal_with_number import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def chinese_only(field):
    a=0
    for ch in field:
        if u'\u4e00' <= ch <= u'\u9fff':
            a = a+1
        else:
            pass
    if a==len(field):
        return 1
    else:
        return 0

def full_to_half(ustring):   #全角转半角
    ustring_ed = ''
    for ustr in ustring:
        ustr_code = ord(ustr)
        if ustr_code == 12288:
            ustr_code = 32
        elif ustr_code >= 65281 and ustr_code <= 65374:
            ustr_code = ustr_code - 65248
        ustr_ed = unichr(ustr_code)
        ustring_ed = ustring_ed+ustr_ed
    return ustring_ed

#非四码使用
def clean_redundancy_special_character(ustring):
    ustring=ustring.replace('\n','').replace('\r','').replace('\t','')
    ustring = ustring.replace(u'\u3000', '').replace(u'\xa0', '').replace(' ', '')
    if "****" not in ustring:
        ustring = ustring.replace('*', '')
    ustring = ustring .replace(u'：', ':').replace('#', '').replace('@', '').replace('$', '').replace('&', '').replace('^', '')
    if len(ustring)==0:
        return ''
    else:
        if (ustring[0] == u"," or ustring[0] == u"，") or (
            (ustring[0] == u"。" or ustring[0] == u".") or ustring[0] == u"?"):

            return ustring[1:]
        else:
            return ustring

#非四码使用
def clean_nothing_chinese(ustring):
    chinese_list=[u"暂缺",u"空",u"无",u"未知","Null","None",u"暂无",u"不详","/","-","--"]
    if ustring in chinese_list:
        return True
    else:
        return False

#清洗pep remark
def clean_pep_remark(ustring):
    for ch in ustring:
        if (u'\u0030' <= ch and ch <= u'\u0039') or (u'\u4e00' <= ch and ch <= u'\u9fff') or ch=="," or ch==u"，" or ch==":" or ch==u"：" or ch==u"。" or ch==u"—" or ch=="-":
            pass
        else:
            ustring = ustring.replace(ch, '')
    return ustring

#清洗pep name\gender\ethnicity\place_of_birth
def clean_pep_n_g_e_p(ustring):
    for ch in ustring:
        if (u'\u4e00' <= ch and ch <= u'\u9fff') or ch==u"·" :  #这些字段只能有汉字和 ‘·’ （部分少数民族的名字），
            pass
        else:
            ustring = ustring.replace(ch, '')
    return ustring

def deal_ethnicity_field(ustring):
    field=''
    ethnicity_list=[u'汉族',u'蒙古族',u'满族',u'朝鲜族',u'赫哲族',u'达斡尔族',u'鄂温克族',u'鄂伦春族',u'回族',u'东乡族',u'土族',u'撒拉族',u'保安族',u'裕固族',u'维吾尔族',u'哈萨克族',u'柯尔克孜族',u'锡伯族',u'塔吉克族',u'乌孜别克族',u'俄罗斯族',u'塔塔尔族',u'藏族',u'门巴族',u'珞巴族',u'羌族',u'彝族',u'白族',u'哈尼族',u'傣族',u'僳僳族',u'佤族',u'拉祜族',u'纳西族',u'景颇族',u'布朗族',u'阿昌族',u'普米族',u'怒族',u'德昂族',u'独龙族',u'基诺族',u'苗族',u'布依族',u'侗族',u'水族',u'仡佬族',u'壮族',u'瑶族',u'仫佬族',u'毛南族',u'京族',u'土家族',u'黎族',u'畲族',u'高山族']
    for ethnicity in ethnicity_list:
        if ethnicity in ustring and u"自治" not in ustring and u"任" not in ustring:
            field=ethnicity

    return field

