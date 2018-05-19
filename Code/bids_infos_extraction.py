#%%
import sys 
sys.path.append("D:\\标签图谱\\标签关系\\bids_infos_extraction\\Code\\")
import os
import pandas as pd
import numpy as np 
import operator
from functools import reduce
from utils import *

key_word_dict = {
    "bid_amount": ["中标金额", "总报价", "中标价", "中标价格", "成交价", "成交价格", "价格"],
    "bid_winner": ["中标公司", "中标单位", "中标供应商", "成交供应商", "谈判成交供应商", "无中标公司信息", 
        "中标人名称", "成交人", "成交人名称", "中标候选人", "成交候选供应商"]
}

a = pd.read_html('../Data/Input/bids_infos_extraction/test2.html', encoding='utf8')
a[0]
#%%
match_result("中标人名称", 3, a[0])