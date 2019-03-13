import hashlib
import random

import time
# from linecache import cache
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf import    models
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, Goods, User, Cart


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
    # 根据index 获取 对应的 分类ID
    categoryid = foodtypes[index].typeid

    # 子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)


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
    # print(childtype_list)
    # print(type(childtype_list))

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


        # 重定向位置
        back = request.COOKIES.get('back')
        # print(back)

        users = User.objects.filter(email=email)
        if  users.exists():
            user = users.first()
            if user.password == generate_password(password):
            # 状态保持
                token = generate_token()
                cache.set(token,user.id,60*60*24)
            # 传递给客户端
                request.session['token'] = token

                # 根据back
                if  back == 'mine':
                    return redirect('axf:mine')
                else:
                    return redirect('axf:marketbase')
            else:
                return render(request, 'login.html', context={'pass_err': '对不起，您输入的密码错误'})
        else:   #密码错误
                return render(request,'login.html',context={'pass_err':'对不起,您输入的用户不存在'})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def addcart(request):
    # 获取token
    token = request.session.get('token')

    # 响应数据
    response_data = {}

    if  token:
        userid = cache.get(token)

        if userid:   #已经登录
            user = User.objects.get(pk=userid)
            goodsid = request.GET.get('goodsid')
            # print(goodsid)
            goods = Goods.objects.get(pk=goodsid)


            carts = Cart.objects.filter(user=user).filter(goods=goods)

            if carts.exists():
                cart = carts.first()
                cart.number = cart.number + 1
                cart.save()

                response_data['status'] = 1
                response_data['msg'] = '添加{}购物车成功:{}'.format(cart.goods.productlongname, cart.number)

                return JsonResponse(response_data)

            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()

                response_data['status'] = 1
                response_data['msg'] = '添加{}购物车成功:{}'.format(cart.goods.productlongname, cart.number)

                return JsonResponse(response_data)
        else:
            return JsonResponse({'msg': '请先登录,后操作', 'status':0})

    else:
        return JsonResponse({'msg':'请先登录,后操作','status':0})


def checkemail(request):
    email = request.GET.get('email')
    print(email)

    # 数据库中查找
    users = User.objects.filter(email=email)
    if  users.exists():
        response_data = {
            'status': 0,
            'msg': '账号不可用'
        }
    else:
      response_data = {
        'status':1,
        'msg':'账号可用'
    }
    return JsonResponse(response_data)