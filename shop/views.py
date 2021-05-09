import json

import requests
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Promotions, Product, Categories
from accounts.models import CustomUser


def start_page(request):
    context = {}
    context.update({'promotions': Promotions.objects.all()})
    context.update({'categories': Categories.objects.all()})
    return render(request, 'start-page.html', context)


def promotion_page(request, promo_id):
    context = {}
    promotion = Promotions.objects.filter(id=promo_id)
    products_list = []
    if promotion.exists():
        promotion = promotion[0]
        if promotion.categories.all().exists():
            for category in promotion.categories.all():
                products = Product.objects.filter(cid=category)
                if products.exists():
                    for product in products:
                        products_list.append(product)
        if promotion.products.all().exists():
            for product in promotion.products.all():
                products_list.append(product)
    context.update({'products': products_list})
    return render(request, 'promotion-page.html', context)


def connect_contact(request):
    return redirect('https://contactguys.herokuapp.com/oauth/?site=aktezor.herokuapp.com/login_contact')


def login_contact(request):
    token = request.GET.get('token')
    result = requests.get('https://contactguys.herokuapp.com/api/user-data/?token='+token)
    dict_user = json.loads(result.text)
    email = dict_user.get('email')
    if not email:
        return redirect('login')
    if CustomUser.objects.filter(email=dict_user['email']).exists():
        user = CustomUser.objects.get(email=dict_user['email'])
        login(request, user)
        return redirect('start_page')
    else:
        user = CustomUser.objects.create(email=dict_user['email'],
                                         first_name=dict_user['first_name'],
                                         last_name=dict_user['last_name'])
        user.save()
        login(request, user)
        return redirect('start_page')


def test_mail(request):
    return render(request,'mail-notify-user.html')
