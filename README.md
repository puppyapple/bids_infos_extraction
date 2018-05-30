# bids_infos_extraction
01-10行：相关库import
12-21行：读取连接库的参数生成mysql数据库连接db
23-26行：默认的查询依据（公告id：announcement_url_id），使用的数据库表名，公告正文对应字段名，公告页html字段名（spider.caigou_announcement_of_award表中没有对公告正文进行清理提取，不存在ggzw_text字段，因此都使用了ggzw_html）
29-49行：文本抽取和表格抽取时各自使用的正则表达式配置表，以嵌套字典储存为全局量，可进行修改、拓展
52-81行：中间函数实现

核心函数：
84-105行：table_info_finder。从公告表格中提取信息，输入参数为html的字符串形式，和表格抽取的正则配置表。返回值为[(comp_name1, value1), (comp_name2, value2),...]的列表，comp_name为中标公司名称，value为中标金额（可能空缺）
107-115行：text_info_finder，从公告文本中提取信息，输出参数为公告文本的字符串形式，和文本抽取的正则配置表。其余同上

查询函数：
117-139行：get_bid_info_conditio, get_bid_info_sqlcondition，自行批量运行测试数据时使用
141-152行：get_bid_info_from_table，根据查询关键字（默认为announcement_url_id）在表中提取数据解析成结果，默认参数值取自上述定义的全局变量，request_key_value为announcement_url_id的字符串形式；返回结果为{announcement_url_id:{result_from_text:[(comp_name1, value1), (comp_name2, value2),...], result_from_table:[(comp_name1, value1), (comp_name2, value2),...]}}的字典形式
154-155行：get_bid_info_from_source，根据公告文本字符串（text）和公告html字符串（html）直接返回{result_from_text:[(comp_name1, value1), (comp_name2, value2),...], result_from_table:[(comp_name1, value1), (comp_name2, value2),...]}；测试时有的表格中有专门对html清洗后的文本字段，因此将如果没有，text和html参数就统一使用html的字符串即可