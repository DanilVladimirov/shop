# Generated by Django 3.1.7 on 2021-04-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subscription_email',
            field=models.BooleanField(default=False),
        ),
    ]