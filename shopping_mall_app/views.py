import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from shopping_mall_app.func_cart import *
from shopping_mall_app.func_goods import *
from shopping_mall_app.function import *


# 登入
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        id = request.POST.get('id')
        password = request.POST.get('password')
        if id == '':
            return render(request, 'login.html', context={'tip': "账号不能为空"})
        if password == '':
            return render(request, 'login.html', context={'tip': "密码不能为空"})
        else:

            if check_userdata(id, password) is True:

                response = redirect(home_page)
                # newuser = json.dumps(username)

                response.set_cookie(key="is_login", value=True, max_age=60 * 60)

                # response.set_cookie(key="username", value=newuser, max_age=60 * 60)

                response.set_cookie(key="id", value=id, max_age=60 * 60)
                return response
            else:
                return render(request, 'login.html', context={'tip': "账号或密码错误"})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        id = request.POST.get("id")
        name = request.POST.get('username')
        pword = request.POST.get('password')
        con_pword = request.POST.get('con_password')
        img = request.FILES.get("head_img")
        head_img = name + "_head"
        # print("************************************************")
        file_name = './static/' + head_img + "." + img.name.split('.')[-1]
        with open(file_name, 'wb+') as f:
            f.write(img.read())
        if '' in [id, name, pword, con_pword]:
            return render(request, 'register.html', context={'key': "麻烦写全"})
        elif pword != con_pword:
            return render(request, 'register.html', context={'key': "密码不一致"})
        elif not username_exist(id):
            return render(request, 'register.html', context={'key': "账号已经存在"})
        insert_into_mysql(id, name, pword, head_img)
        return redirect(login)


# 注销
def login_out(request):
    dict1 = get_goods_info()
    response = render(request, 'home_page.html', dict1)
    response.delete_cookie("is_login")
    id = request.COOKIES.get("id")
    response.delete_cookie(id)
    return response


def login_auth(func):
    def inner(request, *args):
        if request.COOKIES.get("is_login"):
            return func(request, *args)
        else:
            dict1 = get_goods_info()
            dict1["k4"] = "请先登入"
            return render(request, 'home_page.html', dict1)

    return inner


def alter_user_data(request):
    if request.method == 'GET':
        return render(request, 'alter_user_data.html')
    else:
        id = request.POST.get("id")
        password = request.POST.get('password')
        new_username = request.POST.get("new_username")
        new_password = request.POST.get('new_password')
        con_new_password = request.POST.get('con_new_password')
        # print("#################################################################")
        # print(type(user_info), len(user_info))
        if '' in [id, new_username, password, new_password, con_new_password]:
            return render(request, 'alter_user_data.html', context={'key': "麻烦写全"})
        elif check_userdata(id, password) is False:
            return render(request, 'alter_user_data.html', context={'key': "用户名或密码不正确"})
        elif new_password != con_new_password:
            return render(request, 'alter_user_data.html', context={'key': "密码不一致"})
        alter_mysql(id, new_username, new_password)
        return render(request, 'alter_user_data.html', context={'key': "修改完成，请重新登入"})


def add_money(request):
    if request.method == 'GET':
        return render(request, 'add_money.html')
    else:
        id = request.POST.get("id")
        money = request.POST.get("money")
        if '' in [id, money]:
            return render(request, 'add_money.html', context={'key': "麻烦写全"})
        elif username_exist(id) is True:
            return render(request, 'add_money.html', context={"key": "该账号不存在"})
        elif money.isdigit() is False:
            return render(request, 'add_money.html', context={"key": "金额输入有误"})
        else:
            raise_money(id, float(money))
            return render(request, 'add_money.html', context={"key": "充值成功"})


# 后台管理页面
@login_auth
def backgroud_admin(request):
    dict1 = {}
    id = request.COOKIES.get("id")
    username = get_username(id)
    head_img = get_head_img(id)
    power = check_power(id)
    dict1["key1"] = id
    dict1["key2"] = username
    dict1["key3"] = head_img
    if power == 3:
        dict1["key4"] = "超级管理员"
    elif power == 1:
        dict1["key4"] = "会员"
    else:
        dict1["key4"] = "普通用户"
    return render(request, "backgroud_admin.html", context=dict1)


# 上装
@login_auth
def kind_male(request):
    id = request.COOKIES.get("id")
    dict1 = get_male_goods_info()
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"

        return render(request, 'kind_male.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_male.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_male.html', dict1)


# 上装分类
@login_auth
def make_up(request, para):
    id = request.COOKIES.get("id")
    dict1 = get_make_up_goods(para)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_male.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_male.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_male.html', dict1)


# 下装
@login_auth
def kind_female(request):
    id = request.COOKIES.get("id")
    dict1 = get_female_goods_info()
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_female.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_female.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_female.html', dict1)


# 下装分类
@login_auth
def female_goods(request, para):
    id = request.COOKIES.get("id")
    dict1 = get_female_para_goods(para)
    # print(dict1)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_female.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_female.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_female.html', dict1)


# 全部鞋子
@login_auth
def kind_shoes(request):
    id = request.COOKIES.get("id")
    dict1 = get_shoes_goods_info()
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_shoes.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_shoes.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_shoes.html', dict1)


# 鞋子分类
@login_auth
def shoes_goods(request, para):
    id = request.COOKIES.get("id")
    dict1 = get_shoes_para_goods(para)
    # print(dict1)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_shoes.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_shoes.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_shoes.html', dict1)


# 配件
@login_auth
def kind_clothes(request):
    id = request.COOKIES.get("id")
    dict1 = get_clothes_goods_info()
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_clothes.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_clothes.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_clothes.html', dict1)


# 配件分类
@login_auth
def clothes_goods(request, para):
    id = request.COOKIES.get("id")
    dict1 = get_clothes_para_goods(para)
    # print(dict1)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'kind_clothes.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'kind_clothes.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'kind_clothes.html', dict1)


# 显示余额
@login_auth
def show_money(request):
    dict1 = {}
    id = request.COOKIES.get("id")
    username = get_username(id)
    head_img = get_head_img(id)
    money = get_money(id)
    dict1["key1"] = id
    dict1["key2"] = username
    dict1["key3"] = head_img
    dict1["key4"] = money
    return render(request, 'show_money.html', context=dict1)


# 个人中心页面
@login_auth
def personal(request):
    dict1 = {}
    id = request.COOKIES.get("id")
    username = get_username(id)
    head_img = get_head_img(id)
    power = check_power(id)
    dict1["key1"] = id
    dict1["key2"] = username
    dict1["key3"] = head_img
    if power == 3:
        dict1["key4"] = "超级管理员"
    elif power == 1:
        dict1["key4"] = "会员"
    else:
        dict1["key4"] = "普通用户"
    return render(request, "personal.html", context=dict1)


# 主页面
@login_auth
def home_page(request):
    dict1 = get_goods_info()
    id = request.COOKIES.get("id")
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'home_page.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'home_page.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'home_page.html', dict1)


def page(request, para):
    dict1 = get_page(int(para))
    id = request.COOKIES.get("id")
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'home_page.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'home_page.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'home_page.html', dict1)


# 商品详情页
@login_auth
def goods_info(request, para):
    id = request.COOKIES.get("id")
    save_record(id, para)
    dict1 = get_detail_goods_info(para)
    if type(get_assess(para)) == list:
        dict1["key1"] = get_assess(para)
    else:
        dict1["key2"] = get_assess(para)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'goods_info.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'goods_info.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'goods_info.html', dict1)


# 加入购物车
@login_auth
def shopping_cart(request, para):
    id = request.COOKIES.get("id")
    add_goods_to_cart(para, id)
    dict1 = get_detail_goods_info(para)
    dict1["tip"] = "添加成功"
    if type(get_assess(para)) == list:
        dict1["key1"] = get_assess(para)
    else:
        dict1["key2"] = get_assess(para)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'goods_info.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'goods_info.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'goods_info.html', dict1)


# 购物车
@login_auth
def shop_cart_page(request):
    id = request.COOKIES.get("id")
    dict1 = cart_info(id)
    dict1["tip"] = str(sum_money(id))
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'shop_cart_page.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'shop_cart_page.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'shop_cart_page.html', dict1)


# 改变商品数量
@login_auth
def add_goods_num(request, para):
    add_para_goods_num(para)
    return redirect(shop_cart_page)


@login_auth
def reduce_goods_num(request, para):
    reduce_para_goods_num(para)
    return redirect(shop_cart_page)


# 删除购物车某个商品
def del_cart_info(request, para):
    del_cart_para_info(para)
    return redirect(shop_cart_page)


# 支付创建订单
@login_auth
def pay_bill(request):
    id = request.COOKIES.get("id")
    money = get_money(id)
    dict1 = cart_info(id)
    dict1["tip"] = str(sum_money(id))
    if money < sum_money(id):
        if check_power(id) == 3:
            dict1["k1"] = "超级管理员"
            dict1["tip1"] = "余额不足"
            return render(request, 'shop_cart_page.html', dict1)
        elif check_power(id) == 1:
            dict1["k2"] = "会员"
            dict1["tip1"] = "余额不足"
            return render(request, 'shop_cart_page.html', dict1)
        else:
            dict1["k3"] = "普通用户"
            dict1["tip1"] = "余额不足"
            return render(request, 'shop_cart_page.html', dict1)
    else:
        add_order_info(id)
        dict1 = cart_info(id)
        if check_power(id) == 3:
            dict1["k1"] = "超级管理员"
            dict1["tip1"] = "支付成功"
            dict1["tip"] = str(sum_money(id))
            return render(request, 'shop_cart_page.html', dict1)
        elif check_power(id) == 1:
            dict1["k2"] = "会员"
            dict1["tip1"] = "支付成功"
            dict1["tip"] = str(sum_money(id))
            return render(request, 'shop_cart_page.html', dict1)
        else:
            dict1["k3"] = "普通用户"
            dict1["tip1"] = "支付成功"
            dict1["tip"] = str(sum_money(id))
            return render(request, 'shop_cart_page.html', dict1)


# 获取购买记录
@login_auth
def purchase_history(request):
    id = request.COOKIES.get("id")
    dict1 = get_order_info(id)
    return render(request, 'purchase_history.html', dict1)


# 删除购买记录
@login_auth
def del_history(request, para):
    del_order_info(para)
    id = request.COOKIES.get("id")
    dict1 = get_order_info(id)
    return render(request, 'purchase_history.html', dict1)


# 获取浏览记录
@login_auth
def get_record(request):
    id = request.COOKIES.get("id")
    dict1 = get_browse_record(id)
    return render(request, 'get_record.html', dict1)


# 删除浏览记录
@login_auth
def del_record(request, para):
    del_browse_record(para)
    id = request.COOKIES.get("id")
    dict1 = get_browse_record(id)
    return render(request, 'get_record.html', dict1)


# 搜索商品
@login_auth
def search_for_goods(request):
    para = request.POST.get('search')
    id = request.COOKIES.get("id")
    dict1 = search(para)
    if check_power(id) == 3:
        dict1["k1"] = "超级管理员"
        return render(request, 'home_page.html', dict1)
    elif check_power(id) == 1:
        dict1["k2"] = "会员"
        return render(request, 'home_page.html', dict1)
    else:
        dict1["k3"] = "普通用户"
        return render(request, 'home_page.html', dict1)


# 下架商品页
def delete_goods(request):
    dict1 = get_goods_info()
    return render(request, 'delete_goods.html', dict1)


# 下架商品的操作
def del_goods(request, para):
    del_para_goods(para)
    dict1 = get_goods_info()
    return render(request, 'delete_goods.html', dict1)


# 返回shop_store所有商品
def shop_store_goods(request):
    dict1 = get_shop_store_goods()
    return render(request, 'shop_stroe_goods.html', dict1)


# 上架商品
def add_goods(request, para):
    add_to_table_goods(para)
    return redirect(shop_store_goods)


# 修改商品金额
def reset_money(request):
    para1 = request.POST.get('goods_id')
    para2 = request.POST.get('reset_money')
    reset_para_money(para1, para2)
    dict1 = get_goods_info()
    return render(request, 'delete_goods.html', dict1)


# 收入的结算 （包括总收入和某类商品的收入）
def settle_money(request):
    dict1 = settle_account()
    return render(request, 'settle_money.html', dict1)


# 用户的消费记录与消费金额
def user_consume(request):
    dict1 = user_consume_info()
    return render(request, 'user_consume.html', dict1)


# 商品销售信息
def goods_sell(request):
    dict1 = goods_sell_info()
    return render(request, 'goods_sell.html', dict1)


# 评价及评分
def assess(request, para):
    if request.method == 'GET':
        dict1 = {"key1": para}
        return render(request, 'assess.html', dict1)
    else:
        score = request.POST.get("score")
        assess = request.POST.get("assess")
        if score.isdigit() is True:
            if 0 < float(score) < 10:
                set_assess(para, score, assess)
                dict1 = {"key": "评价成功"}
                return render(request, 'assess.html', dict1)
            else:
                dict1 = {"key": "评分：0-10"}
                return render(request, 'assess.html', dict1)

        else:
            dict1 = {"key": "评分：0-10"}
            return render(request, 'assess.html', dict1)
