#coding=utf-8
import time
def zero_only(field):
    a=0
    for ch in field:
        if ch=='0':
            a = a+1
        else:
            pass
    if a==len(field):
        return True
    else:
        return False

def clean_no_chinese_number_character(field):

    for ch in field:
        if ((u'\u0030'<=ch and ch<=u'\u0039') or (u'\u0041'<=ch and ch<=u'\u005A')) or ((u'\u0061'<=ch and ch<=u'\u007A') or (u'\u4e00' <=ch and ch <= u'\u9fff')):
            pass
        else:
            field=field.replace(ch,'')

    return  field

def deal_penalty_decision_date(time_string):
    new_time_string=''
    replace_list = [u'年',u'月','/','\\']
    time_string = time_string.replace(u'零','0').replace(u'一','1').replace(u'二','2').replace(u'三','3').replace(u'四','4').replace(u'五','5').replace(u'六','6').replace(u'七','7').replace(u'八','8').replace(u'九','9')
    for t in time_string:
        if (u'\u0030'<=t and t<=u'\u0039') or t in replace_list or t=='-':
            if t in replace_list:
                t='-'

        else:
            t=''
        new_time_string = new_time_string+t
    if '-' not in new_time_string:
        timeArray = time.localtime(int(new_time_string))
        new_time_string = time.strftime("%Y-%m-%d %H:%M:%S", timeArray).split()[0]
    if 1900<=int(new_time_string.split('-')[0])<=2020:
        return new_time_string
    else:
        return ''
def have_character(strs):
    a=0
    for s in strs:
        if (u'\u0041'<=s and s<=u'\u005A') or (u'\u0061'<=s and s<=u'\u007A'):
            a=1
    if a==1:
        return True
    else:
        return False

def business_registration_code_judgment(code):
    if (len(code)==13 or len(code)==15) and not have_character(code):
        return 'yes'
    else:
        return 'no'

def no_have_character_organization_business_tax(code):
    if not have_character(code):
        return 'yes'
    else:
        return 'no'
