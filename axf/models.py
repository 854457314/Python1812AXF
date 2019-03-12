from django.db import models

# Create your models here.
class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=8)

    class Meta:
        abstract = True


class Wheel(Base):
    class Meta:
        db_table = 'AXF_wheel'


class Nav(Base):
    class Meta:
        db_table = 'AXF_nav'


class Mustbuy(Base):
    class Meta:
        db_table = 'AXF_mustbuy'


class Shop(Base):
    class Meta:
        db_table = 'AXF_shop'

class Mainshow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'AXF_mainshow'


# 分类 模型类
class Foodtype(models.Model):
    # 分类ID
    typeid = models.CharField(max_length=10)
    # 分类名称
    typename = models.CharField(max_length=100)
    # 子类(多个)
    childtypenames = models.CharField(max_length=200)
    # 排序
    typesort = models.IntegerField()

    class Meta:
        db_table = 'AXF_foodtypes'


class Goods(models.Model):
    # 商品ID
    productid = models.CharField(max_length=200)
    # 商品图片
    productimg = models.CharField(max_length=100)
    # 商品名称axf_nav
    productname = models.CharField(max_length=100)
    # 商品长名字
    productlongname = models.CharField(max_length=256)
    # 是否精选
    isxf = models.IntegerField()
    # 是否买一送一
    pmdesc = models.IntegerField()
    # 商品规格
    specifics = models.CharField(max_length=100)
    # 商品价格
    price = models.DecimalField(max_digits=6,decimal_places=2)
    # 商品超市价格
    marketprice = models.DecimalField(max_digits=6, decimal_places=2)
    # 分类ID
    categoryid = models.IntegerField()
    # 子类ID
    childcid = models.IntegerField()
    # 子类名称
    childcidname = models.CharField(max_length=100)
    # 详情页ID
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销售
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'


class  User(models.Model):
    email = models.CharField(max_length=40,unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100,default='axf')
    img = models.CharField(max_length=40,default='axf,png')
    rank = models.IntegerField(default=1)


    class Meta:
        db_table = 'axf:user'
