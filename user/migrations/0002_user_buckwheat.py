# Generated by Django 3.1.5 on 2022-10-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='buckwheat',
            field=models.BooleanField(default=False, verbose_name='메밀'),
        ),
    ]
