from django.shortcuts import render, redirect
from product.models import (Categories,
                            Product,
                            ProductAttrs,
                            Attributes,
                            Brand,
                            CommentsProduct)


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
    return render(request, 'product-page.html', context)
