# Generated by Django 4.2.16 on 2024-11-24 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cart_created_by_alter_orders_user_and_more'),
        ('accounts', '0003_customuser_date_joined_customuser_is_active_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
