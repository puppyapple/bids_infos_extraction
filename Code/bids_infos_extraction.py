# -*- coding: utf-8 -*- 
#%%
import sys 
# sys.path.append("D:\\标签图谱\\标签关系\\bids_infos_extraction\\Code\\")
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
# 中标公告id: announcement_url_id
# 中标金额：total_amount
#%%
key_word_dict = {
    "bid_winner": {
        "step": 3,
        "key_word_list": ["中标公司", "中标单位", "中标供应商", "成交供应商", "谈判成交供应商", "无中标公司信息", 
        "中标人名称", "成交人", "成交人名称", "中标候选人", "成交候选供应商"],
        "regex_list": [".+公司"]
        },
    "bid_amount": {
        "step": 1, 
        "key_word_list": ["中标金额", "总报价", "中标价", "中标价格", "成交价", "成交价格", "价格", "成交金额"],
        "regex_list": [".*"]
        }    
}


html = '../Data/Input/bids_infos_extraction/test2.html'
#%%
# utils.text_info_finder(html, key_word_dict)
utils.table_info_finder(html, key_word_dict)