# -*- coding: utf-8 -*- 
#%%
import os
import pandas as pd
import numpy as np 
import operator
import re
from functools import reduce

# 文本读取
#%%
# 判断词是否至少命中正则规则中的一个
def is_match(word, regex_list):
    return sum([True for regex in regex_list if re.match(regex, word)])

# 返回某个值在dataframe右方和下方step个位置的值列表
def search_around(coord, step, df):
    right_limit = df.shape[1]
    bottom_limit = df.shape[0]
    coords_around = [(coord[0], y) for y in range(coord[1] + 1, min(right_limit, coord[1] + step + 1))] + \
        [(x, coord[1]) for x in range(coord[0] + 1, min(bottom_limit, coord[0] + step + 1))]
    # print(coords_around)
    values_around = [df.values[coo] for coo in coords_around]
    return values_around

# 根据获取全部关键词列表中的词语其右方和下方的数据，经过关键词类别对应的正则规则过滤
def match_result(key_word_list, step, regex_list, df):
    indexes = [np.where(df == key_word) for key_word in key_word_list]
    coordinates = set(reduce(lambda a, b: a + b, [list(zip(ind[0], ind[1])) for ind in indexes]))
    # print(coordinates)
    if len(coordinates) != 0:
        result_raw = reduce(lambda a, b: a + b, [search_around(coo, step, df) for coo in coordinates])
        return [r for r in result_raw if is_match(r, regex_list)]
    else:
        return []

# 根据不同的关键词（抽取主干）进行目标值提取，返回字典列表
def table_info_finder(html_text, key_word_dict):
    try:
        table_list = pd.read_html(html_text, encoding='utf8')
    except ValueError:
        # print("No tables found!")
        return {}
    else:
        result_dict = {k: ",".join(reduce(lambda a, b: a + b, [match_result(v["key_word_list"], v["step"], v["regex_list"], df) for df in table_list])) for k, v in key_word_dict.items()}
        return result_dict

# 文本提取
def text_info_finder(html, key_word_dict):
    return

'''
#%%
df = pd.DataFrame([[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20]])

match_result(8, 3, df)
'''