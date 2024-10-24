# Generated by Django 5.0.1 on 2024-10-23 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0009_alter_product_img_url_alter_product_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img_url',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(max_length=1000),
        ),
    ]
