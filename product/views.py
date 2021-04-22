from django.http import HttpResponse
from django.shortcuts import redirect
from product.models import (Categories,
                            Product,
                            ProductAttrs,
                            Attributes,
                            Brand,
                            CommentsProduct)
from django.shortcuts import render


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
