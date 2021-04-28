from shop.celery import app
from product.models import (Promotions,
                            Product)


@app.task
def stop_promotion(*args, **kwargs):
    promotion = Promotions.objects.get(id=args[0])
    name_promotion = promotion.title
    if promotion.categories.all().exists():
        for category in promotion.categories.all():
            products = Product.objects.filter(cid=category)
            for product in products:
                product.price = product.old_price
                product.old_price = 0
                product.save()
    if promotion.products.all().exists():
        for product in promotion.products.all():
            product.price = product.old_price
            product.old_price = 0
            product.save()
    promotion.delete()
    return f'deleted promotion "{name_promotion}"'
