# -*- coding: utf-8 -*- 
#%%
import os
import pandas as pd
import numpy as np 
import operator
import re
import configparser
import pymysql
from functools import reduce

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

request_key = "announcement_url_id"
table_name = "spider.caigou_html"
text_col_name="ggzw_text"
html_col_name="html"


table_key_word_dict = {
    "bid_winner": {
        "step": 10,
        "key_word_list": [r"^.{0,3}(中标|成交).{0,5}(人|公司|供应商|候选人|单位|候选单位)(名称|信息)?.*$|^供应商(名称|信息).*$", "第一中标候选人", "无中标公司信息"],
        "regex_list": [r".+[公司|学校|研究所|研究院|院|所].*$"]
        },
    "bid_amount": {
        "step": 10, 
        "key_word_list": [r"^.{0,3}(中标|成交|报|总报).{0,5}(价|价格|金额).*"],
        "regex_list": [r"[^\.]*[0-9]+[\.]{0,1}[0-9]+[^\.]*$", "[壹贰叁肆伍陆柒捌玖拾佰仟万亿].*"]
        }    
}

text_key_word_dict = {
    "bid_winner": {
        "expr": (6, r"(((中标|成交).{0,5}(人|公司|供应商|候选人|单位|候选单位)(名称|信息)?|^供应商(名称|信息))[^\u4e00-\u9fa5]{0,10}([\u4e00-\u9fa5]{1,15}[(|（]?[\u4e00-\u9fa5]{1,10}[)|）]?[\u4e00-\u9fa5]{1,15}(公司|学校|研究所|研究院|院|所)))")
        },
    "bid_amount": {
        "expr": (3, r"(总?(中标|成交)总?报?(价格?|金额)[:|：]?(.{1,20}[元|圆][\)|\）]?))") 
        }
}


# 文本读取
#%%
# 判断词是否至少命中正则规则中的一个
def is_match(word, regex_list):
    return sum([True for regex in regex_list if re.match(regex, str(word))])

# 返回某个值在dataframe右方和下方step个位置的值列表
def search_around(coord, step, df):
    right_limit = df.shape[1]
    bottom_limit = df.shape[0]
    # print(right_limit, bottom_limit)
    coords_around = [(coord[0], y) for y in range(coord[1] + 1, min(right_limit, coord[1] + step + 1))] + \
        [(x, coord[1]) for x in range(coord[0] + 1, min(bottom_limit, coord[0] + step + 1))]
    # print(coords_around)
    values_around = [df.values[coo] for coo in coords_around]
    return values_around

# 根据获取全部关键词列表中的词语其右方和下方的数据，经过关键词类别对应的正则规则过滤
def match_result(key_word_list, step, regex_list, df):
    # df_str = df.applymap(lambda x: str(x))
    indexes = [np.where(df.applymap(lambda x: True if re.match(key_word, str(x)) else False)) for key_word in key_word_list]
    coordinates = set(reduce(lambda a, b: a + b, [list(zip(ind[0], ind[1])) for ind in indexes]))
    # print(indexes)
    if len(coordinates) != 0:
        result_raw = reduce(lambda a, b: a + b, [search_around(coo, step, df) for coo in coordinates])
        # print(result_raw)
        return [r for r in result_raw if is_match(r, regex_list)]
    else:
        # print("empty")
        return []

# 根据不同的关键词（抽取主干）进行目标值提取，返回字典列表
def table_info_finder(html_text, key_word_dict):
    try:
        table_list = pd.read_html(html_text, encoding='utf8')
    except ValueError:
        # print("No tables found!")
        return []
    else:
        tb_list = []
        for tb in table_list:       
            tb.dropna(how="all", inplace=True)
            tb.fillna("", inplace=True)
            tb_v = tb.values.tolist()
            tb_v.insert(0, tb.columns)
            tb_list.append(pd.DataFrame(tb_v))
        # print(table_list)
        if len(tb_list) == 0:
            return []
        result_dict = {k: list(reduce(lambda a, b: a + b, [match_result(v["key_word_list"], v["step"], v["regex_list"], df)  \
            for df in tb_list])) for k, v in key_word_dict.items()}
        # print(result_dict)
        if len(result_dict["bid_winner"]) == len(result_dict["bid_amount"]):
            return [(result_dict["bid_winner"][i], result_dict["bid_amount"][i]) for i in range(len(result_dict["bid_winner"]))]
        else:
            return [(result_dict["bid_winner"][i], "") for i in range(len(result_dict["bid_winner"]))]

# 文本提取
def text_info_finder(text, key_word_dict):
    text_str = "".join(text.split())
    result_dict_raw = {k: (v["expr"][0], re.findall(v["expr"][1], text_str)) for k, v in key_word_dict.items()}
    result_dict = {k: [r[v[0]] for r in v[1]] for k, v in result_dict_raw.items()}
    if len(result_dict["bid_winner"]) == len(result_dict["bid_amount"]):
        return [(result_dict["bid_winner"][i], result_dict["bid_amount"][i]) for i in range(len(result_dict["bid_winner"]))]
    else:
        return [(result_dict["bid_winner"][i], "") for i in range(len(result_dict["bid_winner"]))]

# announcement_url_id查询
def get_bid_info_condition(col="announcement_url_id", col_type=str, search_list="all", table_name=table_name, 
        db_con=db, text_key_word_dict=text_key_word_dict, table_key_word_dict=table_key_word_dict):
    sql = ""
    if search_list == "all":
        sql = "select * from %s" % (table_name)
    else:
        condition = ",".join(map(lambda x: "'" + str(x) + "'", search_list)) if col_type == str else ",".join(map(lambda x: str(x), search_list))
        sql = "select * from %s where %s in (%s)" % (table_name, col, condition)
    df = pd.read_sql(sql, con=db_con)
    result = df[["announcement_url_id", "url"]].copy()
    result["result_from_text"] = df["ggzw_text"].apply(lambda x: text_info_finder(x, text_key_word_dict))
    result["result_from_table"] = df["html"].apply(lambda x: table_info_finder(x, table_key_word_dict))
    # result.index = result.announcement_url_id
    # result.drop(["announcement_url_id"], axis=1, inplace=True)
    return result

def get_bid_info_sqlcondition(sqlcondition, table_name=table_name, text_col_name=text_col_name, html_col_name=html_col_name, 
        db_con=db, text_key_word_dict=text_key_word_dict, table_key_word_dict=table_key_word_dict):
    sql = "select * from %s where %s" % (table_name, sqlcondition)
    df = pd.read_sql(sql, con=db_con)
    result = df[["id", "announcement_url_id", "url", "ggzw_text"]].copy()
    result["result_from_text"] = df[text_col_name].apply(lambda x: text_info_finder(x, text_key_word_dict))
    result["result_from_table"] = df[html_col_name].apply(lambda x: table_info_finder(x, table_key_word_dict))
    return result

def get_bid_info_from_table(request_key_value, request_key=request_key, table_name=table_name, text_col_name=text_col_name, html_col_name=html_col_name, 
        db_con=db, text_key_word_dict=text_key_word_dict, table_key_word_dict=table_key_word_dict):
    sql = "select * from %s where %s = '%s'" % (table_name, request_key, request_key_value)
    # print(sql)
    df = pd.read_sql(sql, con=db_con)
    # print(df)
    result = df[["announcement_url_id", "url"]].copy()
    result["result_from_text"] = df[text_col_name].apply(lambda x: text_info_finder(x, text_key_word_dict))
    result["result_from_table"] = df[html_col_name].apply(lambda x: table_info_finder(x, table_key_word_dict))
    result.index = result.announcement_url_id
    result.drop(["announcement_url_id"], axis=1, inplace=True)
    return result.to_dict(orient='index')

def get_bid_info_from_source(text, html, text_key_word_dict=text_key_word_dict, table_key_word_dict=table_key_word_dict):
    return {"result_from_text": text_info_finder(text, text_key_word_dict), "result_from_table": table_info_finder(html, table_key_word_dict)}