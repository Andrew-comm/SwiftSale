# Generated by Django 4.1.5 on 2024-04-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='buying_price',
            field=models.FloatField(default=0),
        ),
    ]
