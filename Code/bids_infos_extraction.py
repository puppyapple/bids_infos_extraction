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


#%%
utils.get_bid_info_from_table("6530025")

#%%
part1 = utils.get_bid_info_sqlcondition("(label_second = '中标公告' or label_three = '中标公告') and announcement_url_id is not null and release_time>'2016-01-01' and release_time<'2017-01-01' limit 6000")
part1
#%%
part2 = utils.get_bid_info_sqlcondition("(label_second = '中标公告' or label_three = '中标公告') and announcement_url_id is not null and release_time>'2017-01-01' and release_time<'2018-01-01' limit 6000")
part3 = utils.get_bid_info_sqlcondition("(label_second = '中标公告' or label_three = '中标公告') and announcement_url_id is not null and release_time>'2018-01-01' limit 2000")
#%% 
result = pd.concat([part1, part2, part3]).to_csv("../Data/Output/bids_infos_extraction/test2.csv")

#%%
len(part1)