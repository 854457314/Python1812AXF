import hashlib
import random

import time
# from linecache import cache
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf import    models
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, Goods, User


def home(request):
    # 轮播图
    wheels = Wheel.objects.all()
    # 导航
    navs = Nav.objects.all()
    # 每日必购
    mustbuys = Mustbuy.objects.all()
    # 商品部分
    shops = Shop.objects.all()
    shophead = shops.first()
    shoptabs = shops[1:3]
    shopclass_list = shops[3:7]
    shopcommends = shops[7:11]

    # 商品列表
    mainshows = Mainshow.objects.all()



    response_str = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptabs':shoptabs,
        'shopclass_list':shopclass_list,
        'shopcommends':shopcommends,
        'mainshows':mainshows,
    }
    return render(request,'home.html',context=response_str)


def market(request, childid='0', sortid='0'):
    # 分类信息
    foodtypes = Foodtype.objects.all()

    index = int(request.COOKIES.get('index', '0'))
    # print(index)
    # 根据index 获取 对应的 分类ID
    categoryid = foodtypes[index].typeid
    # print(categoryid)

    # 子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # print(goods_list)
    # print(type(goods_list))

    # 排序
    # 0默认综合排序   1销量排序     2价格最低   3价格最高
    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

    # 获取子类信息
    childtypenames = foodtypes[index].childtypenames
    # print(childtypenames)
    # 存储子类信息 列表
    childtype_list = []
    # 将对应的子类拆分出来
    for item in childtypenames.split('#'):

        item_arr = item.split(':')
        temp_dir = {
            'name': item_arr[0],
            'id': item_arr[1],
        }

        childtype_list.append(temp_dir)
    print(childtype_list)
    print(type(childtype_list))

    response_dir = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtype_list': childtype_list,
        'childid': childid,
    }


    return render(request, 'market.html', context=response_dir)


def cart(request):
    return render(request,'cart.html')


def mine(request):
    # 获取
    token = request.session.get('token')
    userid = cache.get(token)
    user = None

    if userid:
        user = User.objects.get(pk=userid)

    return render(request, 'mine.html', context={'user': user})


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf8'))
    return md5.hexdigest()


def generate_token():
    temp = str(time.time())+str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf8'))
    return  md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        # 获取数据库
        email = request.POST.get('email')
        name = request.POST.get('name')
        password =  generate_password(request.POST.get('password'))
        # 存入数据库
        user = User()
        user.email = email
        user.password = password
        user.name = name
        user.save()

        # 状态保持
        token = generate_token()

        request.session['token'] = token

        cache.set(token,user.id)


        return redirect('axf:mine')


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)
        if  users.exists():
            user = users.first()
            if user.password == generate_password(password):
            # 状态保持
                token = generate_token()
                cache.set(token,user.id,60*60*24)
            # 传递给客户端
                request.session['token'] = token

                return  redirect('axf:mine')
            else:
                return render(request, 'login.html', context={'pass_err': '对不起，您输入的密码错误'})
        else:   #密码错误
                return render(request,'login.html',context={'pass_err':'对不起,您输入的用户不存在'})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')