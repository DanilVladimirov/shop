# Generated by Django 3.1.7 on 2021-05-07 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
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
            name='PriceMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Name matrix', max_length=200, verbose_name='Название')),
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
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='full_amount_on_curr',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_amount_on_curr',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='cost_on_curr',
        ),
        migrations.AddField(
            model_name='attributes',
            name='title',
            field=models.CharField(default='title', max_length=200),
        ),
        migrations.AddField(
            model_name='delivery',
            name='type_delivery',
            field=models.CharField(choices=[('normal', 'Обычный'), ('np', 'NovaPoshta')], default='normal', max_length=50, verbose_name='Тип (для сторонних интеграций)'),
        ),
        migrations.AddField(
            model_name='order',
            name='cost_of_delivery',
            field=models.FloatField(default=0, verbose_name='Стоимость доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courier', to=settings.AUTH_USER_MODEL, verbose_name='Курьер'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_department',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Информация об адресе доставки.'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.delivery', verbose_name='Способ доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Было ли списание средств.'),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='product.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='file_digit',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл (при тип товара - Файл)'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_recommend',
            field=models.BooleanField(default=False, verbose_name='Рекомендовать'),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='product',
            name='type_product',
            field=models.CharField(choices=[('material', 'Материальный'), ('file', 'Файл')], default='material', max_length=100, verbose_name='Тип товара'),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.currency', verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='full_amount',
            field=models.FloatField(default=0, verbose_name='Полная стоимость товаров в у.е.'),
        ),
        migrations.AlterField(
            model_name='order',
            name='promo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.promocode', verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='order',
            name='rate_currency',
            field=models.FloatField(default=1, verbose_name='Курс валюты в момент заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('processing', 'В обработке'), ('paid', 'Оплачен'), ('finished', 'Завершен'), ('cancel', 'Отменен')], default='new', max_length=50, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=0, verbose_name='Сумма к оплате в у.е.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='productattrs',
            name='value',
            field=models.CharField(default=None, max_length=200),
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
        migrations.AddField(
            model_name='promotions',
            name='products',
            field=models.ManyToManyField(blank=True, to='product.Product'),
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
        migrations.AddField(
            model_name='categories',
            name='key_words',
            field=models.ManyToManyField(to='product.KeyWords'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='matrix',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.pricematrix'),
        ),
    ]
