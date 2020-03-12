import time

import pymysql


def con_mysql():
    return pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', password='123456',
                           db='shopping_mall', charset='utf8')


# 加入购物车
def add_goods_to_cart(para, id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute(
        "insert into cart(goods_id,user_id)values('%s','%s')" % (para, id))
    conn.commit()
    conn.close()
    cursor.close()


# 购物车信息
def cart_info(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select cart_id,goods_id,amount from cart where user_id = '%s'" % (id))
    data = cursor.fetchall()
    li = []
    for i in data:
        sql = "select * from goods where id = '%s'" % (i[1])
        cursor.execute(sql)
        data1 = cursor.fetchall()
        for k in data1:
            tu = k + (i[0], i[2])
            li.append(tu)
    li1 = []
    dict2 = {}
    for j in li:
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
        dict1["key10"] = j[10]
        li1.append(dict1)
    dict2["key"] = li1
    # print(dict2)
    conn.close()
    cursor.close()
    return dict2


# 删除购物车某个商品
def del_cart_para_info(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("delete from cart where cart_id = '%s'" % (para))
    conn.commit()
    conn.close()
    cursor.close()


# 增加商品数量
def add_para_goods_num(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select amount from goods where id = '%s'" % (para))
    data = cursor.fetchall()
    print(data)
    cursor.execute("select amount from cart where goods_id = '%s'" % (para))
    data1 = cursor.fetchall()
    print(data1)
    if data1[0][0] < data[0][0]:
        cursor.execute("update cart set amount=amount+1 where goods_id = '%s'" % (para))
        conn.commit()
    conn.close()
    cursor.close()


# 减少商品数量

def reduce_para_goods_num(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select amount from cart where goods_id = '%s'" % (para))
    data1 = cursor.fetchall()
    print(data1)
    if data1[0][0] > 1:
        cursor.execute("update cart set amount=amount-1 where goods_id = '%s'" % (para))
        conn.commit()
    conn.close()
    cursor.close()


# 某个用户购物车总金额
def sum_money(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select goods_id,amount from cart where user_id = '%s'" % (id))
    data1 = cursor.fetchall()
    conn.close()
    cursor.close()
    sum = 0
    for i in data1:
        conn = con_mysql()
        cursor = conn.cursor()  # 创建游标
        sql = "select price from goods where id = '%s'" % (i[0])
        cursor.execute(sql)
        data2 = cursor.fetchall()
        cursor.close()
        conn.close()
        sum += data2[0][0] * i[1]
    print(sum)
    return sum


# 创建订单信息
def add_order_info(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select goods_id,amount from cart where user_id = '%s'" % (id))
    data = cursor.fetchall()
    # print(data)
    for i in data:
        # print(i[0])
        cursor.execute(
            "insert into order_info(user_id,goods_id,amount,order_time)values('%s','%s','%s',now())" % (
                id, i[0], i[1]))
    cursor.execute(
        "select goods_id,amount from cart where user_id = '%s'" % (id))
    data1 = cursor.fetchall()
    # print(data)
    account = 0
    for i in data1:
        cursor.execute(
            "select price from goods where id = '%s'" % (i[0]))
        data2 = cursor.fetchall()
        account += data2[0][0] * i[1]
    cursor.execute(
        "update user_data set money=money-'%s' where id = '%s'" % (account, id))
    cursor.execute("delete from cart where user_id = '%s'" % (id))
    conn.commit()
    conn.close()
    cursor.close()


# 获取订单信息
def get_order_info(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select order_id,goods_id from order_info where user_id = '%s'" % (id))
    data = cursor.fetchall()
    li1 = []
    for i in data:
        cursor.execute("select * from goods where id = '%s'" % (i[1]))
        data1 = cursor.fetchall()
        if len(data1) != 0:
            data2 = data1[0] + (i[0],)
            li1.append(data2)
        else:
            cursor.execute("delete from order_info where order_id = '%s'" % (i[0]))
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
    return dict2



# 删除订单信息
def del_order_info(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("delete from order_info where order_id = '%s'" % (para))
    conn.commit()
    conn.close()
    cursor.close()


# 收入的结算（总收入和某类商品的收入）
def settle_account():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute(
        "select order_id,goods_id,amount from order_info")
    data = cursor.fetchall()
    li = []
    total, t1, t2, t3, t4 = 0, 0, 0, 0, 0
    dict1 = {}
    for i in data:
        # print(i[1])
        cursor.execute(
            "select kinds,price from goods where id = '%s'" % (i[1]))
        data1 = cursor.fetchall()
        tu = data1[0] + (i[2],)
        li.append(tu)
    print(li)
    for i in li:
        if i[0] == "上装":
            t1 += i[1] * float(i[2])
        if i[0] == "下装":
            t2 += i[1] * float(i[2])
        if i[0] == "配件":
            t3 += i[1] * float(i[2])
        if i[0] == "鞋子":
            t4 += i[1] * float(i[2])
        total += i[1] * float(i[2])
    dict1["key4"] = total
    dict1["key1"] = t1
    dict1["key2"] = t2
    dict1["key3"] = t3
    dict1["key5"] = t4
    conn.commit()
    conn.close()
    cursor.close()
    return dict1




# 评价与评分
def set_assess(*args):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select user_id,goods_id from order_info where order_id = '%s'" % (args[0]))
    data = cursor.fetchall()
    cursor.execute("select order_id from assess where order_id = '%s'" % (args[0]))
    data1 = cursor.fetchall()
    if len(data1) == 0:
        cursor.execute(
            "insert into assess(order_id,user_id,goods_id,assess,score)values('%s','%s','%s','%s','%s')" %
            (args[0], data[0][0], data[0][1], args[2], args[1]))
    else:
        cursor.execute("update assess set assess = '%s',score = '%s' where order_id = '%s'" %
                       (args[2], args[1], args[0]))
    conn.commit()
    conn.close()
    cursor.close()


