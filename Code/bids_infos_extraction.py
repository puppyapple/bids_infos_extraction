# -*- coding: utf-8 -*- 
#%%
import sys 
sys.path.append("D:\\标签图谱\\标签关系\\bids_infos_extraction\\Code\\")
# sys.path.append("/Users/Alexandre/Desktop/Innotree/Graph/bids_infos_extraction/Code")
import os
import pandas as pd
import numpy as np 
import operator
import re
import pymysql
import configparser
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
table_key_word_dict = {
    "bid_winner": {
        "step": 5,
        # "key_word_list": ["中标公司", "中标公司名称" ,"中标单位", "中标单位名称", "中标供应商", "中标供应商名称", 
        # "供应商", "供应商名称", "成交供应商", "成交供应商名称", "谈判成交供应商", "谈判成交供应商名称", "中标人", "中标人名称", 
        # "成交人", "成交人名称", "中标候选人", "中标候选人名称", "成交候选供应商", "成交候选供应商名称", "无中标公司信息"],
        "key_word_list": [r"^.{0,3}(中标|成交).{0,5}(人|公司|供应商|候选人|单位)(名称|信息)?$|^供应商(名称|信息)$", "第一中标候选人", "无中标公司信息"],
        "regex_list": [r".+[公司|学校|研究所|研究院|院|所]$"]
        },
    "bid_amount": {
        "step": 5, 
        # "key_word_list": [".*中标.*金额", ".*总报价", ".*中标价", "中标价格", "成交价", "成交价格", "价格", "成交金额"],
        "key_word_list": [r"^.{0,3}(中标|成交|报|总报).{0,5}(价|价格|金额)"],
        "regex_list": [r"[^\.]*[0-9]+[\.]{0,1}[0-9]+[^\.]*$", "[壹贰叁肆伍陆柒捌玖拾佰仟万亿].*"]
        }    
}

text_key_word_dict = {
    "bid_winner": {
        "expr": (6, r"(((中标|成交).{0,5}(人|公司|供应商|候选人|单位)(名称|信息)?|^供应商(名称|信息))[^\u4e00-\u9fa5]{0,10}([\u4e00-\u9fa5]{1,30}(公司|学校|研究所|研究院|院|所)))")
        },
    "bid_amount": {
        "expr": (3, r"(总?(中标|成交)总?报?(价格?|金额)[:|：]?(.{1,20}[元|圆][\)|\）]?))") # r"(总?(中标|成交)总?报?(价|价格|金额).[^0-9]{0,3}([0-9]+[\.]?[0-9]+.{1,30}[元|圆][\)|\）]?))"
        }
}


#%%
# utils.text_info_finder(html, key_word_dict) .{0,9}(.+[公司|学校|研究所|研究院|院|所])  (?!.*\u4e00-\u9fa5)
html = '../Data/Input/bids_infos_extraction/test2.html'
text = '../Data/Input/bids_infos_extraction/test3.txt'

t = "".join(open(text, encoding='utf8').read().split())
p1 = r"(((中标|成交).{0,2}(人|公司|供应商|候选人|单位)(名称|信息)?|^供应商(名称|信息))[^\u4e00-\u9fa5]{0,10}([\u4e00-\u9fa5]{1,30}(公司|学校|研究所|研究院|院|所)))"
p2 = r"(总?(中标|成交)总?报?(价|价格|金额).[^0-9]{0,3}([0-9]+[\.]?[0-9]+.{1,30}[元|圆][\)|\）]?))"
# re.findall(p1, "加盟中标供应商撒旦法发顺丰公司商认购")
# print(utils.table_info_finder(html, table_key_word_dict), utils.text_info_finder(text, text_key_word_dict))

config = configparser.ConfigParser()
config.read("../Data/Input/database_config/db_spider.conf")
host = config['DATABASE']['host']
user = config['DATABASE']['user']
password = config['DATABASE']['password']
database = config['DATABASE']['database']
port = config['DATABASE']['port']
charset = config['DATABASE']['charset']
db = pymysql.connect(host=host, user=user,
    password=password, db=database, port=int(port), charset=charset)

#%% 
# a = utils.get_bid_info("id", int, [9,10], "spider.zhongbiao", db, text_key_word_dict, table_key_word_dict)
dflist = pd.read_html(html, header=0)
df = dflist[0]
v = df.values.tolist()
v.insert(0, df.columns)
new_df = pd.DataFrame(v)
new_df
utils.match_result(table_key_word_dict["bid_amount"]["key_word_list"], 5, table_key_word_dict["bid_amount"]["regex_list"], new_df)
#%%
# [np.where(df.applymap(lambda x: True if re.match(key_word, str(x)) else False)) for key_word in table_key_word_dict['bid_winner']['key_word_list']]
# for key_word in table_key_word_dict['bid_winner']['key_word_list']:
#     print(key_word)
x = utils.get_bid_info("id", int, "all", "spider.zhongbiao_caigou_html", db, text_key_word_dict, table_key_word_dict)
x.to_csv("../Data/Output/bids_infos_extraction/test.csv")