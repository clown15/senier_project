# Generated by Django 3.1.5 on 2022-10-08 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20221008_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': '상품 사진', 'verbose_name_plural': '상품 사진'},
        ),
        migrations.AlterModelTable(
            name='image',
            table='product_image',
        ),
    ]
