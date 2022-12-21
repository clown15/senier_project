# Generated by Django 3.1.5 on 2022-11-03 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20221030_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergy',
            name='meta_data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='product.metadata', verbose_name='메타데이터'),
            preserve_default=False,
        ),
    ]