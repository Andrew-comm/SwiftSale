# Generated by Django 4.1.5 on 2024-04-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_sale_tax_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
