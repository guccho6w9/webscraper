# Generated by Django 5.0.1 on 2024-10-23 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0008_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img_url',
            field=models.URLField(max_length=600),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(max_length=600),
        ),
    ]
