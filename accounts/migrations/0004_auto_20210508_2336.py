# Generated by Django 3.1.7 on 2021-05-08 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_likes_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='likes_comments',
            new_name='liked_comments',
        ),
    ]