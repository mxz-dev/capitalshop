# Generated by Django 4.2.16 on 2024-12-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cart_created_by_alter_orders_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stock_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
