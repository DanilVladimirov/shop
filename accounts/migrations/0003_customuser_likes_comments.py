# Generated by Django 3.1.7 on 2021-05-08 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210508_2324'),
        ('accounts', '0002_auto_20210508_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='likes_comments',
            field=models.ManyToManyField(to='product.CommentsProduct'),
        ),
    ]