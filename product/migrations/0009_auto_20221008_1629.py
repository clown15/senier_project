# Generated by Django 3.1.5 on 2022-10-08 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20221008_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='main_image',
            new_name='images',
        ),
    ]
