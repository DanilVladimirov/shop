from django.shortcuts import render
from product.models import (Categories,
                            Product,
                            ProductAttrs,
                            Attributes,
                            CommentsProduct,
                            Brand)


def search_products(request):
    search_query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=search_query)
    if products:
        category = products[0].cid.get()
    else:
        category = None
    context = {'category': category,
               'products': products}
    if request.POST:
        dict_request = dict(request.POST)
        products = Product.objects.filter(title__icontains=search_query)
        list_checked = []
        for key, value in dict_request.items():
            attr = Attributes.objects.filter(name=key)
            if len(attr) > 0 and value != 'null':
                products = products.filter(attrs__in=ProductAttrs.objects.filter(value__in=value))
                list_checked += [x for x in value]
        context.update({'checked': list_checked})
        context.update({'products': products})
    return render(request, 'search-products.html', context)
