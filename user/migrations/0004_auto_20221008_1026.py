# Generated by Django 3.1.5 on 2022-10-08 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20221008_0841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allergy',
            options={'verbose_name': '사용자 알러지', 'verbose_name_plural': '사용자 알러지'},
        ),
        migrations.AlterModelTable(
            name='allergy',
            table='user_allergy',
        ),
    ]
