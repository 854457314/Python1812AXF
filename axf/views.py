from django.shortcuts import render

# Create your views here.
from axf.models import Wheel


def home(request):
    # wheels = Wheel.objects.all()
    return render(request,'home.html')


def market(request):
    return render(request,'market.html')


def cart(request):
    return render(request,'cart.html')


def mine(request):
    return render(request,'mine.html')