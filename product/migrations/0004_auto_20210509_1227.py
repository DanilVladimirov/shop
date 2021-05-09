# Generated by Django 3.1.7 on 2021-05-09 12:27

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210509_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=product.models.file_path),
        ),
        migrations.AddField(
            model_name='categories',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=product.models.file_path),
        ),
        migrations.AlterField(
            model_name='presentationimages',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='presentations/<function file_path at 0x7f92778e19d0>'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.FileField(blank=True, default=None, null=True, upload_to='products/<function file_path at 0x7f92778e19d0>'),
        ),
        migrations.AlterField(
            model_name='promotions',
            name='image',
            field=models.ImageField(blank=True, default='promotion_img.jpeg', upload_to=product.models.file_path),
        ),
    ]
