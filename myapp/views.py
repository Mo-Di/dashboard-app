# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from myapp.models import Product
from django.contrib.auth.models import User

import stripe


# Replace with our own key
stripe.api_key = "sk_test_fQeuEvhFtDfTOrpOmtdbyY4a"


def home(request):

    user = request.user
    product_list = stripe.Product.list()['data']
    # product_list = []
    # for prod in products:
    #     if prod.metadata != {} and (prod.metadata["shop"] == user):
    #         product_list.append(prod)
    list_length = len(product_list)
    product_db = Product.objects.filter(shop=user)
    full_list = []
    for item in product_db:
        new_info = Info(item.name, item.description, item.id)
        full_list.append(new_info)
    # for item in range(list_length):
    #     new_info = Info(product_list[item]["name"], product_list[item]["description"], product_list[item]["id"])
    #     full_list.append(new_info)
    full_list.reverse()

    return render(request, 'myapp/home.html', {'full_list':full_list})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})


def logout(request):
    return render(request, 'myapp/login.html')


def create_product(request):
    if request.method == 'POST':

        product = Product()
        product.shop = request.user
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.save()

        new_stripe_product = stripe.Product.create(name=product.name, id=product.id, description=product.description)
        new_stripe_product.metadata["shop"] = product.shop
        new_stripe_product.metadata["price"] = product.price
        new_stripe_product.save()

        return redirect("home")
    else:
        return render(request, 'myapp/home.html')


def query(request):
    product_list = stripe.Product.list()['data']
    list_length = len(product_list)
    query_result = []
    id_list = []
    if request.method == 'POST':
        query_str = request.POST.get("query")
        for item in range(list_length):
            if product_list[item]['name'] == query_str:
                result_item = product_list[item]['name']
                item_id = product_list[item]['id']
                query_result.append(result_item)
                id_list.append(item_id)

        return render(request, 'myapp/query.html', {"list": query_result, "id_list":id_list})


def edit_product(request):
    product_id = request.GET.get("id")
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        return render(request, 'myapp/edit.html', {'product': product})
    else:

        stripe_product = stripe.Product.retrieve(str(product.id))
        if request.POST.get("name"):
            stripe_product["name"] = request.POST.get("name")
            product.name = request.POST.get("name")
        if request.POST.get("description"):
            stripe_product['description'] = request.POST.get("description")
            product.description = request.POST.get("description")
        if request.POST.get("price"):
            stripe_product.metadata["price"] = request.POST.get("price")
            product.price = request.POST.get("price")

        stripe_product.save()
        product.save()
        return redirect('home')


def delete(request):
    if request.GET.get("id"):

        product_id = request.GET.get("id")
        product = Product.objects.get(id=product_id)
        if request.method == "GET":
            return render(request, "myapp/delete.html")
        else:
            stripe_product = stripe.Product.retrieve(str(product.id))
            stripe_product.delete()
            product.delete()
            return redirect("home")
    else:
        return redirect("home")


class Info:
    def __init__(self, name, desc, info_id):
        self.n = name
        self.d = desc
        self.i = info_id
