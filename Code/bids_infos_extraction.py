# -*- coding: utf-8 -*- 
#%%
import sys 
sys.path.append("D:\\标签图谱\\标签关系\\bids_infos_extraction\\Code\\")
import os
import pandas as pd
import numpy as np 
import operator
import re
from imp import reload
from functools import reduce
import utils
reload(utils)

# spider.zhongbiao
# 中标公告id: announcement_url_id(无缺失)
# 采购单位： caigou_unit(无缺失)
# 中标金额：total_amount(部分缺失)
# 中标单位：bid_winner(文本+table)
# 中标单位角色：匹配到的关键字
#%%
key_word_dict = {
    "bid_winner": {
        "step": 3,
        # "key_word_list": ["中标公司", "中标公司名称" ,"中标单位", "中标单位名称", "中标供应商", "中标供应商名称", 
        # "供应商", "供应商名称", "成交供应商", "成交供应商名称", "谈判成交供应商", "谈判成交供应商名称", "中标人", "中标人名称", 
        # "成交人", "成交人名称", "中标候选人", "中标候选人名称", "成交候选供应商", "成交候选供应商名称", "无中标公司信息"],
        "key_word_list": [r"[^无].*[中标|成交].*[人|公司|供应商|候选人|单位][名称|信息]*|供应商[名称|信息]*", "无中标公司信息"],
        "regex_list": [r".+公司$"]    
        },
    "bid_amount": {
        "step": 3, 
        # "key_word_list": [".*中标.*金额", ".*总报价", ".*中标价", "中标价格", "成交价", "成交价格", "价格", "成交金额"],
        "key_word_list": [r"[中标|成交|报|总报].*[价|价格|金额]"],
        "regex_list": [r"[0-9]+[\.]{0,1}[0-9]+[^\.]*$"]
        }    
}

#%%
# utils.text_info_finder(html, key_word_dict)
html = '../Data/Input/bids_infos_extraction/test2.html'
utils.table_info_finder(html, key_word_dict)