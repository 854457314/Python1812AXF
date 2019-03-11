from django.shortcuts import render

# Create your views here.
from axf import    models
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, Goods


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


def market(request):
    # 分类信息
    foodtypes = Foodtype.objects.all()
    # 商品信息
    # goods_list = Goods.objects.all()[0:5]


    index = int(request.COOKIES.get('index','0'))

    categoryid = foodtypes[index].typeid

    goods_list = Goods.objects.filter(categoryid=categoryid)

    response_dir = {
        'foodtypes':foodtypes,
        'goods_list':goods_list,
    }

    return render(request,'market.html',context=response_dir)


def cart(request):
    return render(request,'cart.html')


def mine(request):
    return render(request,'mine.html')