# Generated by Django 3.1.5 on 2022-10-24 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_product_sales_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product'),
        ),
    ]