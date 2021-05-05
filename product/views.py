from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse
from product.models import *
from django.urls import reverse
from django.forms.models import model_to_dict
from product import forms
from accounts import models
from product import services
import json
import requests
from accounts import subscribe
import datetime
from product import convert_html


# for compare strings
def similar(first, second):
    if not len(first) == len(second):
        return False
    if len(first) - sum(l1 == l2 for l1, l2 in zip(first, second)) > 3:
        return False
    return True


def brand_page(request, brand_id):
    context = {'brand': Brand.objects.get(id=brand_id)}
    return render(request, 'brand.html', context)


def search_products(request):
    search_query = request.GET.get('q')
    search_brand = request.GET.get('b')
    search_category = request.GET.get('c')
    products = None
    category = None
    brands = None
    brands_checked = []
    if search_query:
        category = Categories.objects.filter(name__icontains=search_query)
        if category.exists():
            category = Categories.objects.filter(name__icontains=search_query)[0]
            products = Product.objects.filter(cid=category)
            brands = category.brand_set.all()
        else:
            products = Product.objects.filter(title__icontains=search_query)
            if products:
                category = products[0].cid.get()
                brands = category.brand_set.all()
            else:
                # find by brands
                brand = Brand.objects.filter(name__icontains=search_query)
                if brand:
                    return redirect('brand_page', brand_id=brand[0].id)
                else:
                    # find by keywords
                    categories_all = Categories.objects.all()
                    for category_ in categories_all:
                        key_words = category_.key_words.all()
                        list_words = [w.value.lower() for w in key_words]
                        for word in list_words:
                            if similar(search_query.lower().rstrip().lstrip(), word):
                                category = category_
                                products = Product.objects.filter(cid=category)
                                brands = category.brand_set.all()

    # if we have get parameter 'b'
    if search_brand:
        brand = Brand.objects.get(name__icontains=search_brand)
        brands_checked.append(brand)
        category = brand.categories.get(name__icontains=search_category)
        products = brand.product_set.filter(cid=category)
        brands = category.brand_set.all()
    context = {'category': category,
               'products': products,
               'brands': brands,
               'brands_checked': brands_checked}
    if request.POST:
        brands_checked = []
        dict_request = dict(request.POST)
        list_checked = []
        for key, value in dict_request.items():
            attr = Attributes.objects.filter(name=key)
            if len(attr) > 0 and value != 'null':
                products = products.filter(attrs__in=ProductAttrs.objects.filter(value__in=value))
                list_checked += [x for x in value]
        if dict_request.get('brands'):
            for brand in dict_request.get('brands'):
                temp_brand = Brand.objects.get(id=brand)
                products = products.filter(brand=temp_brand)
                brands_checked.append(temp_brand)
        if dict_request.get('price'):
            price_list = [x if x != '' else 0 for x in dict_request.get('price')]
            print(price_list)
            if int(price_list[0]) != 0 or int(price_list[1]) != 0:
                products = products.filter(price__range=(price_list[0], price_list[1]))
            context.update({'price_min': price_list[0]})
            context.update({'price_max': price_list[1]})
        context.update({'brands_checked': brands_checked})
        context.update({'checked': list_checked})
        context.update({'products': products})
    return render(request, 'search-products.html', context)


def product_page(request, pid):
    product = Product.objects.get(id=pid)
    context = {'product': product}
    action = request.POST.get('action')
    if request.POST and action == 'addcom':
        comment = request.POST.get('comment')
        new_comment = CommentsProduct.objects.create(user=request.user,
                                                     text=comment)
        new_comment.save()
        product.comments.add(new_comment)
    if request.POST and action == 'add_to_compare':
        compare_list = request.session.get('compare', {})
        request.session['compare'] = compare_list
        if product.cid.get().name in compare_list:
            if product.id not in compare_list.get(product.cid.get().name):
                temp_values = compare_list[product.cid.get().name]
                temp_values.append(product.id)
                compare_list[product.cid.get().name] = temp_values
        else:
            compare_list[product.cid.get().name] = [product.id]
        request.session.modified = True
        compare_list = request.session.get('compare', {})
        print(compare_list)
    return render(request, 'product-page.html', context)


def compare_page(request, cid):
    action = request.POST.get('action')
    compare_list = request.session.get('compare', {})
    products = []
    context = {}
    print(compare_list)
    if request.POST and action == 'remove':
        product_id = request.POST['product_id']
        list_ = compare_list[cid]
        list_.remove(int(product_id))
        if len(list_) == 0:
            del request.session['compare'][cid]
        else:
            request.session['compare'][cid] = list_
    if compare_list.get(cid):
        products_list = compare_list.get(cid)
        for product_id in products_list:
            products.append(Product.objects.get(id=product_id))
    request.session.modified = True
    context.update({'products': products})
    return render(request, 'compare-page.html', context)


def del_category(request):
    compare_list = request.session.get('compare', {})
    if request.POST:
        del compare_list[request.POST['category']]
        request.session['compare'] = compare_list
        print(compare_list)
    return HttpResponse('')


def seller_products(request):
    if not request.user.groups.filter(name='Seller').exists():
        return redirect('start_page')
    action = request.POST.get('action')
    context = {}
    products = Product.objects.filter(author=request.user)
    context.update({'products': products})
    if request.POST and action == 'edit_menu':
        product_to_edit = Product.objects.get(id=request.POST.get('pid'))
        attributes = Categories.objects.get(id=product_to_edit.cid.get().id).attributes.all()
        context.update({'product_edit': product_to_edit})
        context.update({'attributes': attributes})
    if request.POST and action == 'edit':
        brand = Brand.objects.get(id=request.user.brand.id)
        category = Product.objects.get(id=request.POST.get('pid')).cid.get()
        attributes = category.attributes.values()
        product = Product.objects.filter(id=request.POST.get('pid'))
        product.update(title=request.POST.get('prod_name'),
                       brand=brand,
                       price=float(request.POST.get('prod_price')),
                       author=request.user)
        list_attrs = []
        for attr in attributes:
            prod_attr = ProductAttrs.objects.get(fkey_attr_id=attr['id'], value=request.POST.get(str(attr['id'])))
            list_attrs.append(prod_attr)
        product[0].attrs.set(list_attrs)

    if request.POST and action == 'create':
        categories = Categories.objects.all()
        context.update({'categories': categories})
    if request.POST and action == 'choosed_category':
        attributes = Categories.objects.get(id=request.POST.get('cid')).attributes.all()
        context.update({'choosed': Categories.objects.get(id=request.POST.get('cid'))})
        context.update({'attributes': attributes})
        categories = Categories.objects.all()
        context.update({'categories': categories})
    if request.POST and action == 'create_product':
        attributes = Categories.objects.get(id=request.POST.get('cid')).attributes.values()
        category = Categories.objects.get(id=request.POST.get('cid'))
        brand = Brand.objects.get(id=request.user.brand.id)
        product = Product.objects.create(title=request.POST.get('prod_name'),
                                         brand=brand,
                                         price=float(request.POST.get('prod_price')),
                                         author=request.user)
        product.cid.set([category])
        if category not in brand.categories.all():
            brand.categories.add(category)
        for attr in attributes:
            prod_attr = ProductAttrs.objects.filter(fkey_attr_id=attr['id'],
                                                    value=request.POST.get(str(attr['id'])))
            if len(prod_attr) > 0:
                product.attrs.add(prod_attr[0])
            else:
                prod_attr = ProductAttrs.objects.create(fkey_attr_id=attr['id'],
                                                        value=request.POST.get(str(attr['id'])))
                prod_attr.save()
                product.attrs.add(prod_attr)
        product.save()
    if request.POST and action == 'delete':
        Product.objects.get(id=request.POST.get('pid')).delete()
    return render(request, 'seller-products.html', context)


def shop_main_page(request):
    categories = Categories.objects.all()
    return render(request, 'product/main_page.html', context={'category':categories})


def category_page(request, pk):
    category = Product.objects.filter(cid=pk)
    return render(request, 'product/category_page.html', context={'products':category})


def product_page_new(request, pk):
    context = {}
    viewed_products = request.session.get('viewed_products', {})
    product = get_object_or_404(Product, pk=pk)
    viewed_products.pop(str(product.id), None)
    if len(viewed_products) >= 6: del viewed_products[next(iter(viewed_products))]
    viewed_products_html = convert_html.viewed_products(viewed_products)
    context['product'] = product
    viewed_products[str(product.id)] = {'id':product.id, 'title':product.title, 'price':product.price, 'desc':product.desc}
    request.session['viewed_products'] = viewed_products
    context['viewed_products'] = viewed_products_html
    if request.user.is_authenticated:
        try:
            context['is_wishlist']=product.wishlist_set.get(user = request.user)
        except Wishlist.DoesNotExist:
            context['is_wishlist'] = False
        try:
            context['is_sub_edit_price']=product.subeditprice_set.get(user = request.user)
        except SubEditPrice.DoesNotExist:
            context['is_sub_edit_price']=False

    return render(request, 'product/product_page.html', context)


def select_curr(request):
    if request.method == 'POST':
        link = request.META.get('HTTP_REFERER')
        request.session['curr_id'] = request.POST.get('all_currency')
        return HttpResponseRedirect(link)

def basket(request):
    if request.method == 'POST':
        
        basket = services.Basket.get_basket(request.user.id) if request.user.is_authenticated else request.session.get('basket', {})
        type_basket = request.POST.get('type')
        product_id = request.POST.get('id')
        check_promo = request.POST.get('promocode')
        data_response={}
        product_cnt = request.POST.get('cnt', 1)
        product_cnt = 1 if not product_cnt else product_cnt   
        if type_basket == 'add':
            basket = services.Basket.add2basket(basket, product_id, product_cnt, user_id=request.user.id)
            data_response = {'success': f'Добавлено в корзину {product_cnt} товаров'}
        elif type_basket == 'del':
            basket = services.Basket.del2basket(basket, product_id, request.user.id)
            html_result = ""
            count_items = 1
            for product_val in basket.values():
                id_product = product_val['id']
                html_result += f'<tr><th scope="row">{count_items}</th>'
                html_result += f'<td><a href=\'{reverse("product_page", kwargs={"pk":id_product})}\'">{product_val["title"]}</a></td>'
                html_result += f'<td>посчитать</td>'
                html_result += f'<td>{product_val["qty"]}</td>'
                html_result += f'<td><button type=\'submit\' onclick="del_basket({id_product})">X</button></td>'
                html_result += '</tr>'
                count_items+=1
                    
            html_result += ''
            data_response = {'success':'Удалено', 'responce':html_result}
        elif check_promo:
            promo = Promocode.objects.filter(code = check_promo).first()
            if promo:
                sum_discount = promo.get_sum_discount(basket['full_sum_basket'])
                if sum_discount:
                    total_sum = round((basket['full_sum_basket'] + sum_discount)*request.session['rate_curr'], 2)
                    data_response = {'success':total_sum}
                else:
                    data_response={'error':'Промо не найден.'}
            else:
                data_response={'error':'Промо не найден.'}
            
        request.session['basket'] = basket

        return HttpResponse(json.dumps(data_response), content_type = 'application/json')


def checkout_page(request):
    basket = services.Basket.get_basket(request.user.id) if request.user.is_authenticated else request.session.get('basket', {})
    total_cost = sum([i['qty'] * i['price'] for i in basket.values()])
    delivery = Delivery.objects.all()
    if request.method == 'POST':
        data = request.POST.copy()
        id_delivery = data.get('delivery')
        order_delivery = Delivery.objects.get(pk=id_delivery)
        order_currency = Currency.objects.get(code = request.session.get('curr_id', 'UAH'))
        promocode = data.get('promo_code')
        is_promo = False
        if promocode:
            is_promo = Promocode.is_promo(data.get('promo_code'))
            if is_promo:
                data['promo'] = Promocode.objects.get(code = data['promo_code'])
        data['user'] = request.user if request.user.is_authenticated else ''
        data['currency'] = order_currency
        data['rate_currency'] = order_currency.rate
        data['delivery_method'] = order_delivery
        create_order = forms.OrderForm(data)
        print(create_order.errors)

        if create_order.is_valid() and basket:
            new_order = create_order.save()
            if request.user:
                subscribe.subscribe_create_order(request.user.id, new_order.id, new_order.get_absolute_url())
            for good in basket.values():
                item = {
                    'product': Product.objects.get(pk=good['id']),
                    'order': new_order,
                    'qty': good['qty'],
                }
                OrderItem.add_item(item)
                new_order.recalc_order()

            return redirect('invoice_page', new_order.id)  

    return render(request, 'product/checkout_page.html', context={'products':basket, 'total_cost':total_cost, 'all_delivery':delivery})


def get_invoice(request, pk):
    template = 'product/invoice_page.html'
    context = {}
    order = get_object_or_404(Order, pk=pk)
    goods = order.orderitem_set.all()
    digital_links = {}
    if order.status == 'paid':
        for good in goods:
            product_in_inv = get_object_or_404(Product, pk = good.id_good)
            type_good = product_in_inv.type_product
            if type_good == 'file':
                link_product_file = product_in_inv.file_digit.url
                digital_links[good.title_good] = link_product_file
    if request.user.is_authenticated and order.user:
        if request.user.id == order.user.id:
            user_balance = order.user.balance
            if user_balance >= order.total_amount and order.status != 'paid':
                context['pay'] = True

    if order.is_paid and request.user.has_perm('product.change_status'):
        context['cancel_order'] = True

    if request.method == 'POST':
        data = request.POST
        meta = data.get('mode')
        if meta == 'pay_order':
            if context.get('pay'):
                context['pay'] = not order.payment()
        elif meta=='cancel_order' and context.get('cancel_order'):
                context['cancel_order'] = not order.cancel_order()
                context['pay'] = True

    context['order'] = order
    context['goods'] = goods
    context['digital'] = digital_links
    return render(request, template, context=context)


def edit_invoice(request, pk):
    template = 'product/invoice_edit_page.html'
    context = {}
    order = get_object_or_404(Order, pk=pk)
    goods = order.orderitem_set.all()
    context['order'] = order
    if request.method == 'POST':
        mode  = request.POST.get('mode') 
        data = request.POST
        if mode == 'edit_invoice':
            for good in goods:
                try:
                    edit_price = float(data.get(f'price_{good.id}'))
                    edit_qty = int(data.get(f'qty_{good.id}'))
                    del_good = data.get(f'del_{good.id}')
                except ValueError:
                    break
                if edit_price and edit_qty:
                    if del_good:
                        OrderItem.objects.get(pk = good.id).delete()
                        continue
                    
                    item_info={
                        'pk':good.id,
                        'price':edit_price,
                        'qty':edit_qty,
                    }
                    OrderItem.add_item(item_info)
            goods = order.orderitem_set.all()
        
        elif mode == 'add_good':
            product = get_object_or_404(Product, pk=pk)
            item_info = {
                'product':product,
                'order':order,
            }
            OrderItem.add_item(item_info)
        order.recalc_order()
    context['goods'] = goods

    return render(request, template, context=context)


def wishlist(request):
    if request.method == 'POST':
        data_response = {}
        data = request.POST
        type_action = data.get('type')
        product = get_object_or_404(Product, pk = data.get('id'))
        if type_action == 'add':
            item, create = Wishlist.objects.get_or_create(
                user = request.user,
                product = product,
            )
            if create:
                data_response['success'] = {'msg':'Товар добавлен в список желаний'}
            else:
                data_response['error'] = {'msg':'Товар уже в списке желаний'}
        elif type_action == 'del':
            try:
                Wishlist.objects.get(
                    user = request.user, 
                    product = product,
                ).delete()
                data_response['success'] = {'msg':'Товар удален из списка желаний'}
            except Wishlist.DoesNotExist:
                data_response['error'] = {'msg':'Товар не найден в списке желаний'}
        elif type_action=='del_for_wishlist':
            try:
                Wishlist.objects.get(
                    user = request.user, 
                    product = product,
                ).delete()
                wishlist = Wishlist.objects.filter(user = request.user)
                data_response['success'] = convert_html.my_wishlist(wishlist)
            except Wishlist.DoesNotExist:
                data_response['error'] = {'msg':'Товар не найден в списке желаний'}
        return HttpResponse(json.dumps(data_response), content_type = 'application/json')


    elif request.method == 'GET':
        context = {}
        template = 'product/wishlist.html'
        wishlist = Wishlist.objects.filter(user = request.user)
        context['products'] = convert_html.my_wishlist(wishlist) 
        return render(request, template, context)


def subeditprice(request):
    if request.method == 'POST':
        data_response = {}
        data = request.POST
        type_action = data.get('type')
        product = get_object_or_404(Product, pk = data.get('id'))
        if type_action == 'add':
            item, create = SubEditPrice.objects.get_or_create(
                user = request.user,
                product = product,
            )
            if create:
                data_response['success'] = {'msg':'Товар добавлен в подписки'}
            else:
                data_response['error'] = {'msg':'Ты уже подписан'}
        elif type_action == 'del':
            try:
                SubEditPrice.objects.get(
                    user = request.user, 
                    product = product,
                ).delete()
                data_response['success'] = {'msg':'Подписка отменена'}
            except SubEditPrice.DoesNotExist:
                data_response['error'] = {'msg':'Товар не найден в подписках'}
        return HttpResponse(json.dumps(data_response), content_type = 'application/json')
