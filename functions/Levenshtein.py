#coding=utf-8
from __future__ import division  #实数化除法
import time

start_time = time.time()
end_time = time.time()

def levenshtein(str_1,str_2):
    len_1 = len(str_1)
    len_2 = len(str_2)
    dp_list = []

    for i in range(0, len_1 + 1):
        dp_list.append([])
        dp_list[i].append(i)

    for i in range(1, len_2 + 1):
        dp_list[0].append(i)

    for i in range(1, len_1 + 1):
        for j in range(1, len_2 + 1):
            if str_1[i - 1] == str_2[j - 1]:
                dp_list[i].append(dp_list[i - 1][j - 1])
            else:
                dp_mark = min(dp_list[i - 1][j - 1], min(dp_list[i][j - 1], dp_list[i - 1][j])) + 1
                dp_list[i].append(dp_mark)

    return str((1-dp_list[len_1][len_2]/max(len_2,len_1))*100)+' %'

def list_str_levenshtein(list_str):
    for i in range(0,len(list_str)-1):
        for j in range(i, len(list_str)):
            score = levenshtein(list_str[i],list_str[j])
            print list_str[i]+' | '+list_str[j]+u'  相似度得分是：'+score


list_str_levenshtein(['hduehuehd','udehdue','dhuehdueh','gdyegggu'])

