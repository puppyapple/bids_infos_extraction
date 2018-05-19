# -*- coding: utf-8 -*- 
#%%
import os
import pandas as pd
import numpy as np 
import operator
from functools import reduce
# spider.zhongbiao
# 中标时间: date_award 
# 中标金额：total_amount

#%%
def search_around(coord, step, df):
    right_limit = df.shape[1]
    bottom_limit = df.shape[0]
    coords_around = [(coord[0], y) for y in range(coord[1] + 1, min(right_limit, coord[1] + step + 1))] + \
        [(x, coord[1]) for x in range(coord[0] + 1, min(bottom_limit, coord[0] + step + 1))]
    # print(coords_around)
    values_around = [df.values[coo] for coo in coords_around]
    return values_around

def match_result(key_word, step, df):
    indexes = np.where(df == key_word)
    coordinates = list(zip(indexes[0], indexes[1]))
    # print(coordinates)
    result = reduce(lambda a,b: a + b, [search_around(coo, step, df) for coo in coordinates])
    return result

def amount_in_table(df, word_dict):
    return

def table_info_finder(html_text, key_word_dict):
    table_list = pd.read_html(html_text, encoding='utf8')
    return
'''
#%%
df = pd.DataFrame([[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20]])
df
#%%
match_result(8, 3, df)
'''