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
utils.get_bid_info_from_table("9826431")
