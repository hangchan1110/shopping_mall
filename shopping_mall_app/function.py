import pymysql


def con_mysql():
    return pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', password='123456',
                           db='shopping_mall', charset='utf8')


# 插入用户名，密码，头像
def insert_into_mysql(id, username, password, head_img):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute(
        "insert into user_data(id,username,password,head_img) values('%s','%s','%s','%s')" % (id, username,
                                                                                              password, head_img))
    conn.commit()
    conn.close()
    cursor.close()


# 验证用户名是否已经存在
def username_exist(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select id from user_data where id = '%s'" % (id))
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    if len(data) == 0:
        return True
    else:
        return False


# 查看用户的权限
def check_power(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select power from user_data where id = '%s'" % (id))
    data = cursor.fetchall()
    print(data)
    conn.close()
    cursor.close()
    return data[0][0]


# 验证用户名和密码是否正确
def check_userdata(id, pw):
    """
    检验账号和密码是否正确
    :param name: 账号
    :param pw: 密码
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', password='123456',
                           db='shopping_mall', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    for i in data:
        if id == i[0] and pw == i[2]:
            print(i[0], i[2])
            return True
    else:
        return False


# 修改用户密码，个人简介，头像
def alter_mysql(*args):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("update user_data set username='%s' where id = '%s'" % (args[1], args[0]))
    cursor.execute("update user_data set password='%s' where id = '%s'" % (args[2], args[0]))
    conn.commit()
    conn.close()
    cursor.close()


def get_head_img(id):
    """
    返回头像
    :param username:
    :return:
    """
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select head_img from user_data where id = '%s'" % (id))
    data = cursor.fetchall()
    conn.close()
    return data[0][0]


def get_money(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select money from user_data where id = '%s'" % (id))
    data = cursor.fetchall()
    conn.close()
    return data[0][0]


def get_username(id):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select username from user_data where id = '%s'" % (id))
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    return data[0][0]


def raise_money(*args):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("update user_data set money=money+'%d' where id = '%s'" % (args[1], args[0]))
    conn.commit()
    conn.close()
    cursor.close()


# 删除该用户信息
def del_user_data(name):
    """
    删除用户信息
    :param name:
    :return:
    """
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("delete from user.user_data where username = '%s'" % (name))
    conn.commit()
    conn.close()
    cursor.close()


# 搜索商品
def search(para):
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    cursor.execute("select * from goods where instr(goods_intro,'%s')" % (para))
    data = cursor.fetchall()
    conn.close()
    cursor.close()
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


# 返回shop_store所有商品
def get_shop_store_goods():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select * from shop_store"
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


#  # 某个用户的消费记录与消费金额
def user_consume_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select distinct user_id from order_info"
    cursor.execute(sql)
    data = cursor.fetchall()
    dict1 = {}
    dict2 = {}
    for i in data:
        count = 0
        cursor.execute("select  order_id,goods_id,amount from order_info where user_id = '%s'" % (i[0]))
        data1 = cursor.fetchall()
        for j in data1:
            cursor.execute("select  * from goods where id = '%s'" % (j[1]))
            data2 = cursor.fetchall()
            for k in data2:
                count += k[5] * j[2]
                dict1[i[0]] = count
    dict2["key"] = dict1
    sql = "select * from order_info"
    cursor.execute(sql)
    data3 = cursor.fetchall()
    li = []
    for i in data3:
        sql = "select * from goods where id = '%s'" % (i[2])
        cursor.execute(sql)
        data4 = cursor.fetchall()
        tu = data4[0] + (i[0], i[1], i[3], i[4])
        li.append(tu)
    li1 = []
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
        dict1["key11"] = j[11]
        dict1["key12"] = j[12]
        li1.append(dict1)
    dict2["key1"] = li1
    cursor.close()
    # 关闭连接
    conn.close()
    return dict2


# 商品销售信息
def goods_sell_info():
    conn = con_mysql()
    cursor = conn.cursor()  # 创建游标
    sql = "select goods_id,amount from order_info"
    cursor.execute(sql)
    data = cursor.fetchall()
    li = []
    dic = {}
    for i in data:
        if i[0] in dic.keys():
            dic[i[0]] = dic[i[0]] + i[1]
        else:
            dic[i[0]] = i[1]
    list1 = [(k, v) for k, v in dic.items()]
    for i in list1:
        sql = "select * from goods where id = '%s'" % i[0]
        cursor.execute(sql)
        data1 = cursor.fetchall()
        tu = data1[0] + (i[1],)
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
        li1.append(dict1)
    dict2["key"] = li1
    cursor.close()
    # 关闭连接
    conn.close()
    return dict2
