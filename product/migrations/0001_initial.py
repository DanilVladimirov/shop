# Generated by Django 3.1.7 on 2021-05-08 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(default='title', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname cat', max_length=250, unique=True)),
                ('state', models.BooleanField(default=True)),
                ('attributes', models.ManyToManyField(to='product.Attributes')),
            ],
        ),
        migrations.CreateModel(
            name='CommentsProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='Текст')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(blank=True, max_length=15)),
                ('rate', models.FloatField(default=1)),
                ('disp', models.CharField(blank=True, default='y.e.', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Delivery', max_length=350)),
                ('type_delivery', models.CharField(choices=[('normal', 'Обычный'), ('np', 'NovaPoshta')], default='normal', max_length=50, verbose_name='Тип (для сторонних интеграций)')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryCitiesNP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('city_ua', models.CharField(blank=True, max_length=150, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('region_ua', models.CharField(blank=True, max_length=200, null=True)),
                ('city_ref', models.CharField(blank=True, max_length=50, null=True)),
                ('cityID', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='KeyWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_amount', models.FloatField(default=0, verbose_name='Полная стоимость товаров в у.е.')),
                ('total_amount', models.FloatField(default=0, verbose_name='Сумма к оплате в у.е.')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'Новый'), ('processing', 'В обработке'), ('paid', 'Оплачен'), ('finished', 'Завершен'), ('cancel', 'Отменен')], default='new', max_length=50, verbose_name='Статус заказа')),
                ('rate_currency', models.FloatField(default=1, verbose_name='Курс валюты в момент заказа')),
                ('cost_of_delivery', models.FloatField(default=0, verbose_name='Стоимость доставки')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Было ли списание средств.')),
                ('delivery_department', models.CharField(blank=True, max_length=400, null=True, verbose_name='Информация об адресе доставки.')),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Номер телефона')),
                ('full_name', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Адрес доставки')),
                ('notes', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Комментарий к заказу')),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courier', to=settings.AUTH_USER_MODEL, verbose_name='Курьер')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.currency', verbose_name='Валюта')),
                ('delivery_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.delivery', verbose_name='Способ доставки')),
            ],
            options={
                'permissions': (('change_status', 'Can change status order'),),
            },
        ),
        migrations.CreateModel(
            name='PresentationImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='presentations')),
            ],
        ),
        migrations.CreateModel(
            name='PriceMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Name matrix', max_length=200, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_product', models.CharField(choices=[('material', 'Материальный'), ('file', 'Файл')], default='material', max_length=100, verbose_name='Тип товара')),
                ('file_digit', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл (при тип товара - Файл)')),
                ('title', models.CharField(default='Noname', max_length=300)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
                ('desc', models.TextField(blank=True, default='', null=True)),
                ('vendor_code', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('old_price', models.FloatField(blank=True, default=0, null=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_edit', models.DateTimeField(auto_now=True)),
                ('photo', models.FileField(blank=True, default=None, null=True, upload_to='')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='Рекомендовать')),
                ('rating', models.FloatField(blank=True, null=True, verbose_name='Рейтинг')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
            ],
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, unique=True)),
                ('type_code', models.CharField(choices=[('fixed', 'Фиксированная'), ('relative', 'Относительная')], default='fixed', max_length=50)),
                ('amount_of_discount', models.FloatField(default=0)),
                ('type_promo', models.CharField(choices=[('onceuse', 'Одноразовые'), ('reusable', 'Многоразовые')], default='reusable', max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('start_promo', models.DateField(blank=True, null=True)),
                ('end_promo', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('discount_percentage', models.FloatField(default=0.0)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('image', models.ImageField(blank=True, default='promotion_img.jpeg', upload_to='')),
                ('categories', models.ManyToManyField(blank=True, to='product.Categories')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('show_all_wishlist', 'Просматривать список желаний других пользователей'),),
            },
        ),
        migrations.CreateModel(
            name='SubEditPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubActivateProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RatingProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_product', to='product.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PromotionsTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_end_id', models.TextField(default='')),
                ('task_start_id', models.TextField(default='')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.promotions')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default=None, max_length=200)),
                ('fkey_attr', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.attributes')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='attrs',
            field=models.ManyToManyField(to='product.ProductAttrs'),
        ),
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='cid',
            field=models.ManyToManyField(related_name='category', to='product.Categories'),
        ),
        migrations.AddField(
            model_name='product',
            name='comments',
            field=models.ManyToManyField(blank=True, to='product.CommentsProduct'),
        ),
        migrations.AddField(
            model_name='product',
            name='presentation_images',
            field=models.ManyToManyField(blank=True, to='product.PresentationImages'),
        ),
        migrations.CreateModel(
            name='PriceMatrixItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_value', models.FloatField(default=0, verbose_name='От')),
                ('max_value', models.FloatField(default=0, verbose_name='До')),
                ('type_item', models.CharField(choices=[('relative', 'В процентах'), ('fixed', 'Фиксированная')], default='fixed', max_length=50, verbose_name='Тип')),
                ('value', models.FloatField(default=0, verbose_name='Значение')),
                ('matrix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.pricematrix')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_good', models.IntegerField(default=1)),
                ('title_good', models.CharField(default='Noname', max_length=300)),
                ('cost', models.FloatField(default=1)),
                ('qty', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.order')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='promo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.promocode', verbose_name='Промокод'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FileTelegram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_file', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryWarehousesNP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitekey', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, default='', max_length=250)),
                ('description_ru', models.CharField(blank=True, default='', max_length=250)),
                ('short_address', models.CharField(blank=True, default='', max_length=250)),
                ('short_address_ru', models.CharField(blank=True, default='', max_length=250)),
                ('ref_warehouse', models.CharField(blank=True, default='', max_length=250)),
                ('number_warehouse', models.IntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.deliverycitiesnp')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='matrix',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.pricematrix'),
        ),
        migrations.AddField(
            model_name='categories',
            name='key_words',
            field=models.ManyToManyField(to='product.KeyWords'),
        ),
        migrations.AddField(
            model_name='categories',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.categories'),
        ),
        migrations.AddField(
            model_name='brand',
            name='categories',
            field=models.ManyToManyField(to='product.Categories'),
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1, verbose_name='Количество')),
                ('price', models.FloatField(verbose_name='Стоимость за ед.')),
                ('date_add', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'permissions': (('show_all_baskets', 'Просматривать корзины других пользователей'),),
            },
        ),
    ]