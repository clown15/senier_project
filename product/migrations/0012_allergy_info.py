# Generated by Django 3.1.5 on 2022-10-15 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20221008_1026'),
        ('product', '0011_auto_20221008_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buckwheat', models.BooleanField(default=False, verbose_name='메밀')),
                ('wheat', models.BooleanField(default=False, verbose_name='밀')),
                ('Big_head', models.BooleanField(default=False, verbose_name='대두')),
                ('peanut', models.BooleanField(default=False, verbose_name='땅콩')),
                ('Walnut', models.BooleanField(default=False, verbose_name='호두')),
                ('pine_nut', models.BooleanField(default=False, verbose_name='잣')),
                ('peach', models.BooleanField(default=False, verbose_name='복숭아')),
                ('tomato', models.BooleanField(default=False, verbose_name='토마토')),
                ('milk', models.BooleanField(default=False, verbose_name='우유')),
                ('shrimp', models.BooleanField(default=False, verbose_name='새우')),
                ('Mackerel', models.BooleanField(default=False, verbose_name='고등어')),
                ('squid', models.BooleanField(default=False, verbose_name='오징어')),
                ('crab', models.BooleanField(default=False, verbose_name='게')),
                ('clam', models.BooleanField(default=False, verbose_name='조개')),
                ('Pork', models.BooleanField(default=False, verbose_name='돼지고기')),
                ('beef', models.BooleanField(default=False, verbose_name='쇠고기')),
                ('chicken', models.BooleanField(default=False, verbose_name='닭고기')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '상품 알러지 정보',
                'verbose_name_plural': '상품 알러지 정보',
                'db_table': 'product_allergy',
            },
        ),
    ]
