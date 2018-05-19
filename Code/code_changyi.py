# -*- coding: utf-8 -*-
import csv


# 固定截取某一字段区间的信息
def ie(a,texttest):
    # len = len(texttest.split(a))
    list3 = []
    for index ,i in enumerate(texttest.split(a)):
        if index == 0:
            continue
        # if "采购" in i:
        #     continue
        if "公司" in i:
            if "采购代理" in i:
                continue
            list2 = i.split("公司")[0]
            list2 += "公司"
            if ":" in list2:
                list2 = list2.strip(":").strip()
            elif "：" in list2:
                list2 = list2.strip("：").strip()
            else:
                list2.strip()
            list3.append(list2.strip("名称:").strip("中标金额(人民币元)").strip("成交金额(人民币元)").strip("：").strip(":").strip())
        else:
            continue
        return list3

dict = ["中标公司", "中标单位", "中标供应商", "中标供应商名称", "成交供应商名称", "成交供应商", "谈判成交供应商", "无中标公司信息", "中标人名称", "成交人", "中标候选人", "成交候选供应商"]

out = open('output13_4.csv', 'w')

# csv文件写入时的表头，通常为一个列表
headers = ['ID', '公告标题', '关联公司', '角色', "公告时间", "源地址"]
# 在定义csv_write时需要把文件名与表头同时加入
csv_writer = csv.DictWriter(out, fieldnames=headers)
# 在写入csv文件前，需要writeheader() 做初始化处理
csv_writer.writeheader()

import pymysql

# 打开数据库连接
db = pymysql.connect(host="172.31.215.44", user="weichangyi", 
    password="GkHKjVq11J7aNTZ72m9", db="spider", port=3306, charset="utf8")

# 使用cursor()方法获取操作游标
cur = db.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select * from spider.zhongbiao_caigou_html"
# sql = "select * from spider.zhongbiao "
try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    print("id", "ggzw_text")
    # 遍历结果
    i = 0
    for row in results:
        # print(type(row))
        id = row[0]

        l4 = row[4]
        text = row[11]
        text = text.strip().replace("\t", " ").replace("\n", " ").replace(" ", "")
        list1 = []
        for t in dict:
            if t in text:
                try:
                    # print(id,l4,ie(t, "：", text),t)
                    list1.append(t)
                    list12 = ie(t,text)
                    # count1 = text.count(t)
                    if id == 5814:
                        print(list12, text)
                    if id == 6635:
                        print(list12, text)
                    if id == 6735:
                        print(list12, text)
                        # print(id, l4, ie(t, ":", text), t)
                    csv_writer.writerow({'ID': id, '公告标题': l4, '公告时间': row[8], '关联公司': list12,
                                         '角色': list1, '源地址': row[6]})
                    i += 1
                    continue
                except IndexError:
                    continue
            else:
                pass
    print(i)
    out.close()
except Exception as e:
    raise e
finally:
    db.close()