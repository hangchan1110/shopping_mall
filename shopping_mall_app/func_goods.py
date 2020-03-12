import json
from math import ceil

import pymysql


def con_mysql():
    return pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', password='123456',
                           db='shopping_mall', charset='utf8')


# 插入商品信息
def add_goods_to_mysql(*args):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute(
        "insert into goods(kinds,category,goods_name,size,price,goods_img,goods_intro,amount)values(%s','%s','%s','%s','%f','%s','%s','%d')" %
        (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]))
    conn.commit()
    conn.close()
    cursor.close()


# 返回所有商品相关信息
def get_goods_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods limit %s,%s" % (0, 12)
    cursor.execute(sql)
    data = cursor.fetchall()
    sql_1 = "select id from goods "
    cursor.execute(sql_1)
    data1 = cursor.fetchall()
    l = len(data1)
    # print(l)
    page_num = int(ceil(l / 12))
    li1 = list(range(1, page_num + 1))
    # print(li)
    cursor.close()
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    dict2["page"] = li1
    # print(dict2)
    return dict2


def get_page(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods limit %s,%s" % (13 * para - 13, 12)
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    sql_1 = "select id from goods "
    cursor.execute(sql_1)
    data1 = cursor.fetchall()
    l = len(data1)
    # print(l)
    page_num = int(ceil(l / 12))
    li1 = list(range(1, page_num + 1))
    # print(li)
    cursor.close()
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    dict2["page"] = li1
    return dict2




# # 上装
def get_male_goods_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '上装'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 上装分类
def get_make_up_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '上装'and category = '%s'" % (para)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    # print(data)
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 下装
def get_female_goods_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '下装'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 下装 分类 短裤 长裤
def get_female_para_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '下装'and category = '%s'" % (para)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 返回鞋子
def get_shoes_goods_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '鞋子'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 返回鞋子 运动鞋
def get_shoes_para_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '鞋子'and category = '%s'" % (para)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    # print(data)
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 返回配件
def get_clothes_goods_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '配件'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 配件分类 篮球 背包 袜子 帽子
def get_clothes_para_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where kinds = '配件' and category = '%s'" % (para)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    # print(data)
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 返回商品详细信息
def get_detail_goods_info(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from goods where id = '%s'" % (para)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    # print(data)
    li = []
    dict2 = {}
    for j in data:
        # print(i)
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        li.append(dict1)
    dict2["key"] = li
    return dict2


# 保存浏览商品记录
def save_record(id, para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute(
        "insert into browse_record(user_id,goods_id)values('%s','%s')" % (id, para))
    conn.commit()
    conn.close()
    cursor.close()


# 获取浏览记录
def get_browse_record(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select record_id,goods_id from browse_record where user_id = '%s'" % (id))
    data = cursor.fetchall()
    # print(data)
    li1 = []
    for i in data:
        cursor.execute("select * from goods where id = '%s'" % (i[1]))
        data1 = cursor.fetchall()
        if len(data1) != 0:
            data2 = data1[0] + (i[0],)
            li1.append(data2)
        else:
            cursor.execute("delete from browse_record where record_id = '%s'" % (i[0]))

    dict2 = {}
    li2 = []
    for j in li1:
        dict1 = {}
        dict1["key0"] = j[0]
        dict1["key1"] = j[1]
        dict1["key2"] = j[2]
        dict1["key3"] = j[3]
        dict1["key4"] = j[4]
        dict1["key5"] = j[5]
        dict1["key6"] = j[6]
        dict1["key7"] = j[7]
        dict1["key8"] = j[8]
        dict1["key9"] = j[9]
        li2.append(dict1)
    dict2["key"] = li2
    conn.commit()
    conn.close()
    cursor.close()
    # print(dict2)
    return dict2


# 删除浏览记录
def del_browse_record(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("delete from browse_record where record_id = '%s'" % (para))
    conn.commit()
    conn.close()
    cursor.close()


# 下架商品
def del_para_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("delete from goods where id = '%s'" % (para))
    conn.commit()
    conn.close()
    cursor.close()


# 上架商品
def add_to_table_goods(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select * from shop_store where goods_id = '%s'" % (para))
    data = cursor.fetchall()

    # print(data)
    li = []
    for i in data[0]:
        li.append(i)
    # print(li)
    cursor.execute(
        "insert into goods(kinds,category,goods_name,size,price,goods_img,goods_intro,amount)values('%s','%s','%s','%s','%s','%s','%s','%d')" %
        (pymysql.escape_string(li[1]), pymysql.escape_string(li[2]), pymysql.escape_string(li[3]),
         pymysql.escape_string(li[4]), float(li[5]), pymysql.escape_string(li[6]),
         pymysql.escape_string(li[7]), int(li[8])))
    conn.commit()
    conn.close()
    cursor.close()


# 修改商品的金额
def reset_para_money(id, money):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "update goods set price = '%s' where id = '%s'" % (money, id)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


# 获取评价和评分
def get_assess(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select * from assess where goods_id = '%s'" % (para))
    data = cursor.fetchall()
    if len(data) == 0:
        return "暂无评价"
    else:
        li = []
        for j in data:
            dict1 = {}
            dict1["key0"] = j[0]
            dict1["key1"] = j[1]
            dict1["key2"] = j[2]
            dict1["key3"] = j[3]
            dict1["key4"] = j[4]
            li.append(dict1)
        # print(dict2)
        return li


