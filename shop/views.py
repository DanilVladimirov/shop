from django.shortcuts import render
from product.models import Promotions, Product


def start_page(request):
    context = {}
    context.update({'promotions': Promotions.objects.all()})
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
