# Generated by Django 4.2.16 on 2024-11-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_products_discount_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
