# Generated by Django 3.1.5 on 2022-10-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_product_buckwheat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='ėí ėŽė§'),
        ),
    ]
