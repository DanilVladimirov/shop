from shop.celery import app
from product.models import (Promotions,
                            Product,
                            CustomUser)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


SHOP_MAIL = 'aktezorshop@gmail.com'


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


@app.task
def start_promotion(*args, **kwargs):
    promotion = Promotions.objects.get(id=args[0])
    list_products = []
    if promotion.categories.all().exists():
        for category in promotion.categories.all():
            products = Product.objects.filter(cid=category)
            for product in products:
                product.old_price = product.price
                product.price = product.price - (product.price * promotion.discount_percentage)
                product.save()
                list_products.append(product.title)
    if promotion.products.all().exists():
        for product in promotion.products.all():
            product.old_price = product.price
            product.price = product.price - (product.price * promotion.discount_percentage)
            product.save()
            list_products.append(product.title)
    users = CustomUser.objects.all()
    # send mail
    separator = ", "
    text = f'The promotion is valid for these products: {separator.join(list_products)}.' \
           f'\nPromotion ends: {promotion.date_end}'
    html_content = render_to_string('mail_promotion_template.html', {'title': promotion.title,
                                                                     'text': text,
                                                                     'img_src': promotion.image.url})
    text_content = strip_tags(html_content)
    list_users = [user.email for user in users if user.subscription_email]
    if len(list_users) > 0:
        send_email.apply_async(args=(promotion.title, text_content, list_users, html_content))
    return f'started promotion "{promotion.title}"'


# 0 - title
# 1 - html
# 2 - user_mails (must be list)
# 3 - html-content
@app.task
def send_email(*args, **kwargs):
    email = EmailMultiAlternatives(args[0], args[1], SHOP_MAIL, args[2])
    email.attach_alternative(args[3], "text/html")
    email.send()
    return f'already send mails to {args[2]}'
